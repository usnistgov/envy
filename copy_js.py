"""
A script to collect JS files from within the dependent libraries and dump them in js folder for packaging
"""

def pull_from_submodules():
    """
    Pull js files from submodules
    """
    import os, shutil
    # paths relative to externals/threejs
    relpaths = [
        "build/three.min.js",
        "examples/js/math/Lut.js",
        "examples/js/geometries/TextGeometry.js",
        "examples/js/utils/FontUtils.js",
        "examples/js/controls/OrbitControls.js",
        "examples/fonts/helvetiker_regular.typeface.js",
        "examples/js/libs/stats.min.js"
    ]
    if not os.path.exists('js'):
        os.mkdir('js')
    else:
        try:
            shutil.rmtree('js')
            os.mkdir('js')
        except:
            raise
            #raise ValueError('Unable to delete js directory')

    for path in relpaths:
        old_name = os.path.join('externals/threejs',path)
        apath, fname = os.path.split(old_name)
        new_name = os.path.join('js', fname)
        shutil.copy2(old_name, new_name)

def pull_jquery():
    """
    In order to avoid the dependency on building jquery and jquery UI, 
    we just download a stable version of jquery
    """
    urls = [
        ('http://code.jquery.com/jquery-1.10.2.js', 'js/jquery.js'),
        ('http://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css','js/jquery-ui-smoothness.css'),
        ('http://code.jquery.com/ui/1.11.4/jquery-ui.js', 'js/jquery-ui.js'),
    ]
    import urllib
    for url, ofname in urls:
        
        handle = urllib.urlopen(url)
        with open(ofname,'w') as fp:
            fp.write(handle.read())

if __name__=='__main__':
    pull_from_submodules()
    #pull_jquery()
