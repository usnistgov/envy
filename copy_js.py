"""
A script to collect JS files from within the dependent libraries and dump them in js folder for packaging
"""

if __name__=='__main__':
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
