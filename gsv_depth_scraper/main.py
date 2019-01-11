import requests, os, shutil, time, json, zipfile
from numpy.random import random_sample
import gsv_depth_scraper.pano, gsv_depth_scraper.dpth, gsv_depth_scraper.xform, gsv_depth_scraper.geom


# --------------------
# "scrape" mode
# --------------------    
def gjpts_to_panos(pth_geo, api_key, pth_wrk, name, zoom=3, fmt="png", delay=False, limit=False): 
    print("loading coords from geojson: {}".format(pth_geo))
    gpts = gsv_depth_scraper.geom.load_gpts(pth_geo)
    if limit:
        print("limiting loaded coords from {} to {}".format(len(gpts),limit))
        gpts = gpts[:limit]
    
    panoids = gsv_depth_scraper.pano.gpts_to_panoids(gpts, api_key) # panoids are unique
    print("parsed {} sample locations and found {} unique panoids".format(len(gpts),len(panoids)))
    for n, panoid in enumerate(panoids):
        pano_img = gsv_depth_scraper.pano.panoid_to_img(panoid, api_key, zoom)
        if not pano_img: continue
        
        dpth_inf = gsv_depth_scraper.dpth.panoid_to_depthinfo(panoid)
        if pano_img and dpth_inf:
            #print("==== {} of {} \t{}\t{} planes\tmax_depth: {}".format(n, len(panoids), panoid, len(dpth_inf['planes']),max(dpth_inf['depth_map'])))
            print("==== {} of {} \t{}".format((n+1), len(panoids), panoid))
            pano_img.save(os.path.join(pth_wrk,"{}.{}".format(panoid,fmt))) # save pano
            with open(os.path.join(pth_wrk,'{}.json'.format(panoid)), 'w') as f: 
                json.dump(dpth_inf, f, separators=(',', ':')) # save depth data
        else:
            print("!!!! FAILED\t{}".format(panoid))
        if delay:
            jitter = ((random_sample()-0.5)*2) * delay * 0.3 # +/- 30% of delay
            print("... pausing for {0:.2f}s".format(delay + jitter))
            time.sleep(delay + jitter)

    return True
    
# --------------------
# "process" mode
# --------------------
def panos_to_tile_package(pth_wrk, pth_zip, name, fmt="png"):
    
    # create ZIP archive object
    zipobj = zipfile.ZipFile(pth_zip, 'w', zipfile.ZIP_DEFLATED)
    
    print("loading panos from working directory and archiving: {}".format(pth_wrk))
    panoids, pano_imgs = gsv_depth_scraper.pano.load_panos_and_package_to_zip(pth_wrk, zipobj, fmt)
    
    print("creating images from depthmap data and archiving")
    metadata, dpth_imgs = gsv_depth_scraper.dpth.load_dpths_and_package_to_zip(panoids, pth_wrk, zipobj)
            
    pair_count = len(panoids)
    print("cutting tiles for {} depthpanos".format(pair_count))
    
    for n, (panoid, pano_img, dpth_img) in enumerate(zip(panoids, pano_imgs, dpth_imgs)):
        #panoid, pano_img, dpth_img = item[0], item[1]['pano'], item[1]['dpth']
        tic = time.clock()
        gsv_depth_scraper.xform.cut_tiles_and_package_to_zip(dpth_img, "dpth", panoid, zipobj, fmt, gsv_depth_scraper.xform.face_size(pano_img))
        gsv_depth_scraper.xform.cut_tiles_and_package_to_zip(pano_img, "pano", panoid, zipobj, fmt)
        toc = time.clock()
        dur = int(toc-tic)
        print("cutting tiles for {} ({}/{}) took {}s. at this rate, {}s ({:.2f}m) to go.".format(panoid, n+1, pair_count, dur, (pair_count-(n+1))*dur, ((pair_count-(n+1))*dur)/60.0 ))
    
    print("packaged {} depthpanos to {}.\nthe working directory may now be deleted: {}".format(pair_count, pth_zip, pth_wrk))



def _prepare_working_directory(dir, name, delete_existing=False):
    pth_dest = os.path.join(dir, name)
    pth_zip = os.path.join(dir,"{}.zip".format(name))
    
    if delete_existing:
        if not os.path.isdir(pth_dest): os.mkdir(pth_dest)
        else:
            for f in os.listdir(pth_dest):
                fpth = os.path.join(pth_dest, f)
                try:
                    if os.path.isfile(fpth): os.unlink(fpth)
                    elif os.path.isdir(fpth): shutil.rmtree(fpth)
                except Exception as e:
                    print(e)
                    raise Exception("Contents of the specified working directory could not be deleted in preparation for the scrape. Are they in use?")
    else:
        if not os.path.isdir(pth_dest): 
            raise Exception("The working directory does not contain existing data by this name.")
            
    return pth_dest, pth_zip