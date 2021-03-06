
import matplotlib.pyplot as plt
import networkx as nx
import csv
import os

import numpy as np

CSV_PATH = "./data/random-generated-graph-data.csv"
IMG_PATH = "./data/random-generated-graph-img/"


'''
============================================================
Based on chapter 1 of the paper
		Characterization of Complex Networks:
			  A Survey of measurements
============================================================

'''

# Data Saving
def safe_path_relative(save_path):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), save_path)
    # if(not os.path.exists(path)):
    #     raise Exception("Given path {0} is not a directory".format(save_path))

    return path

def csv_writer(name=CSV_PATH):
    path = safe_path_relative(name)

    csv_binary = open(path, "wb")
    writer = csv.writer(csv_binary, delimiter=',', quotechar='\'', quoting=csv.QUOTE_NONE)
    return writer

def savegraph(G, pos, save_path):
    path=safe_path_relative(save_path)
    plt.clf()
    nx.draw(G,pos, node_color="#A0CBE2", width=4)
    plt.savefig(path.format(save_path),format="PNG")

def save_csv(header,data, writer):
    writer.writerow(header)
    writer.writerows(data)

# Incides in Matrix
N = 0
P = 1
AVG_CLUSTERING   = 1

MAXITER_AVGING = 10
MAXITER = 10
LOWER = 1
HIGHER = 10

def extract_dimensions(
    B,
    x_ind=0,
    y_ind=1,
    z_ind=2):
    x = B[:,:,x_ind]

    y = B[:,:,y_ind]

    z = B[:,:,z_ind]

    return (x,y,z)

# Aggregators
def collect_raw(
    collector,
    n_range, p_size, p_samples):

    # If both are zero
    if((n_range[0]+n_range[1])==0):
        n_range=(1,1)

    # If the first is 0 then make it 1
    if(n_range[0]==0):
        n_range[0]=1

    # If second is greater than the first
    if(n_range[0]>n_range[1]):
         n_range=(n_range[1],n_range[0])

    n_s, n_e = n_range
    fract = 1/float(p_size)

    def avg_ps(n,p):
        ttl = 0
        for x in xrange(1,p_samples):
            ttl=ttl+collector(nx.fast_gnp_random_graph(n,fract*p))
        avg = ttl/p_samples
        return [n,p,avg]

    A = [
         [avg_ps(n,p) for p in xrange(1,p_size+1)]
          for n in xrange(n_s,n_e+1)
        ]

    return A

def correlate(Z):
    data = collect_raw(
        Z,
        (LOWER,HIGHER),
        MAXITER,
        MAXITER_AVGING)

    return extract_dimensions(np.array(data))
