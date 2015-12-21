import CoolProp, math, numpy as np, matplotlib.pyplot as plt, json, pandas, os

pair = ['PROPANE','DECANE']

input_data = dict(N = 21, backend = 'REFPROP', fluid1 = pair[0], fluid2 = pair[1], p_cutoff = 7e4)

from scipy.interpolate import interp1d as Interpolate

HEOS = CoolProp.AbstractState(input_data['backend'],input_data['fluid1'] + '&' + input_data['fluid2'])

X0 = np.linspace(0.00001, 0.99999, input_data['N'])

meshes = []
for iii in range(input_data['N']-1):

    n = 500
    data = []
    for x0 in [X0[iii], X0[iii+1]]:

        HEOS.set_mole_fractions([x0, 1 - x0])
        try:
            HEOS.build_phase_envelope("dummy")
        except ValueError as VE:
            print(VE)
        
        PE = HEOS.get_phase_envelope_data()
        
        # Find maximum pressure location
        ipmax = np.argmax(PE.p)

        # Interpolate to find densities corresponding to cutoff pressure (if possible)
        if np.min(PE.p[0:ipmax-1]) < input_data['p_cutoff'] < np.max(PE.p[0:ipmax-1]):
            rhoymin = Interpolate(PE.p[0:ipmax-1], PE.rhomolar_vap[0:ipmax-1], kind = 'quadratic')([input_data['p_cutoff']])[0]
        else:
            rhoymin = np.min(PE.rhomolar_vap)*1.0000001
        rhoymin = max(np.min(PE.rhomolar_vap), rhoymin)

        if np.min(PE.p[ipmax+1::]) < input_data['p_cutoff'] < np.max(PE.p[ipmax+1::]):
            pvap = np.array(PE.p[ipmax+1::])
            rhoyvap = np.array(PE.rhomolar_vap[ipmax+1::])
            rhoymax = 1/Interpolate(np.log(pvap), 1/rhoyvap, kind = 'linear')([np.log(input_data['p_cutoff'])])[0]
        else:
            rhoymax = np.max(PE.rhomolar_vap)*0.9999999
        rhoymax = min(np.max(PE.rhomolar_vap), rhoymax)

        rhoy = np.logspace(math.log10(rhoymin), math.log10(rhoymax), n)
        T = Interpolate(np.array(PE.rhomolar_vap), PE.T, kind = 'linear')(rhoy)
        logp = Interpolate(1/np.array(PE.rhomolar_vap), np.log(PE.p), kind = 'linear')(1/rhoy)

        data.append((list(T), list(logp), rhoy))

    # Stitch the left (in composition) and right (in composition) parts together
    T = data[0][0] + data[1][0]
    logp = data[0][1] + data[1][1]
    z = list(X0[iii]*np.ones_like(data[0][0])) + list(X0[iii+1]*np.ones_like(data[0][0]))

    facets = []
    for i in range(0, n-1):
        # The two triangles formed by this square
        facets += [0+i, 1+i, 0+n+i, -1, 0+n+i, 1+i, 1+n+i, -1]

    # vertices are of the form: x1, y1, z1, x2, y2, z2, ... - no connection is implied
    vertices = []
    for _x, _y, _z in zip(T, np.array(logp)*50, np.array(z)*100):
        vertices += [_x, _y, _z]

    meshes.append(dict(vertices = vertices, facets = facets))

with open('env.json','w') as fp:
    json.dump(meshes, fp)

VLE_data_file = r'C:\Users\ihb\Documents\NIST\BinaryFitter\all_VLE_data_reconciled.csv'
if os.path.exists(VLE_data_file):
    df = pandas.read_csv(VLE_data_file)
    mask = df['fluid[0] (-)'].isin(pair) & df['fluid[1] (-)'].isin(pair) & (df['Ncomp (-)'] == 2) & (df['p (Pa)'] < 1e15) & (df['p (Pa)'] > 0) & (~np.isnan(df['x[0] (-)'])) & (np.isnan(df['y[0] (-)']) | ((0 < df['y[0] (-)']) & (df['y[0] (-)'] < 1)))
    df = df[mask].copy()
    T,p,x = df['T (K90)'], df['p (Pa)'], 1-df['x[0] (-)']

    metadata = []
    for _T, _p, _x in zip(T, p, x):
        metadata.append('T: {0:g} K<br>p: {1:g} kPa<br>x<sub>1</sub>: {2:g}'.format(_T, _p/1000.0, _x))

    jj = dict(x = T.tolist(), y = (np.log(p)*50).tolist(), z = (x*100).tolist(), r = np.ones_like(x).tolist(), metadata = metadata)

    with open('spheres.json','w') as fp:
        json.dump(jj, fp)
else:
    print('WARNING: Unable to load VLE data to generate spheres.json')