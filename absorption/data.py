
import numpy as np

NP_SIZE = 50

NUM_CELL_LIVER = int( 2.5 * 1.38*10**8 ) # grams of liver * cells/g
PER_KUP_LIVER = 0.15 # percentage of cells that are Kupffer cells in the liver
NUM_KUP = NUM_CELL_LIVER * PER_KUP_LIVER # number of Kuppfer cells
NUM_REC_PER_CELL = 2.*10**4 # average receptors per cell
NUM_REC_KUP = NUM_REC_PER_CELL * NUM_KUP # number of receptors on all kuppfer cells

print(NUM_CELL_LIVER*0.15, NUM_REC_KUP)

def dose2number(dose, np_size):
    #dose in surface area, cm**2
    return int( ( dose*10**14 ) / ( 4*np.pi*np_size**2 ) )

SPECIES = { 4: 'liver', 5 : 'tumor'}

DOSE = {
        dose2number(62, NP_SIZE) : { 0 : {  'liver' :  [0.000000, 0.000000, 0.000000], 'tumor' : [0.000000, 0.000000, 0.000000] }, 2 : {  'liver' :  [50.345970, 39.209410, 27.359930], 'tumor' : [0.263281, 0.1393019, 0.1196472] }, 8 : { 'liver' : [76.277370, 46.693370, 71.837720, 75.873670, 78.654550, 78.614840], 'tumor' : [0.0803674, 0.8498338, 0.1303301] }, 24: {  'liver' : [88.898410, 56.429970, 60.216400],'tumor' : [1.041616, 0.3949728, 0.5819533] }}  ,
        dose2number(15708, NP_SIZE) : { 0 : {  'liver' :  [0.000000, 0.000000, 0.000000], 'tumor' : [0.000000, 0.000000, 0.000000] }, 2 : {  'liver' :  [10.520040, 8.692864, 9.124880], 'tumor' : [2.606629, 2.710481, 2.058090] }, 8 : {  'liver' :  [21.695960, 21.083590, 20.495130], 'tumor' : [5.046099, 3.660958, 7.019610] }, 24: {  'liver' :  [27.289000, 27.957120, 28.039000], 'tumor' : [31.513000, 30.803710, 7.524036, 12.658530, 18.477020, 21.026080] }} }
        # how do I average Ben's data?

FINAL_DOSE = { dose2number(15, NP_SIZE) : { 24 : {  'liver' :  [42.710910, 3.764380, 45.784530, 34.931660, 73.842140, 61.928360], 'tumor' : [0.4397003, 4.600060, 0.3063612, 2.130397, 3.781415, 1.910672] }},
               dose2number(62, NP_SIZE) : { 24 : { 'liver' :  [51.947590, 53.760490, 58.019490, 46.178190, 74.409670, 77.982170], 'tumor' : [4.673019, 2.159501, 4.719816, 7.230515, 1.136087, 2.700611] }},
               dose2number(245, NP_SIZE) : { 24 : { 'liver' :  [36.623010, 49.519400, 37.541030], 'tumor' : [17.442330, 1.80961, 7.741403, 14.768600, 17.046230, 18.642470] }},
               dose2number(983, NP_SIZE) : { 24 : { 'liver' :  [40.520700, 33.917760, 36.027190, 38.804620, 60.262840, 40.454190], 'tumor' : [15.425270, 16.405680, 15.668590, 13.801590, 11.601200, 15.429100] }},
               dose2number(3927, NP_SIZE) : { 24 : { 'liver' :  [22.089350, 23.890780, 21.090850], 'tumor' : [5.865150, 10.433240, 18.819230, 17.521080, 21.329250, 19.203240] }},
               dose2number(15708, NP_SIZE) : { 24 : { 'liver' :  [27.289000, 27.957120, 28.039000], 'tumor' : [31.513000, 30.803710, 7.524036, 12.658530, 18.477020, 21.026080] }} }

print(dose2number(12,NP_SIZE), dose2number(15708, NP_SIZE))
