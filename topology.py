#!/usr/bin/env python3
"""
Custom Multi-Path Topology for SDN + Socket Programming Mini-Project
Topology:
    h1 --- s1 --- s2 --- s4 --- h2   (Primary Path)
             \         /
              --- s3 --              (Backup Path)
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

class MultiPathTopo(Topo):
    def build(self):
        # 1. Add Hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')

        # 2. Add OpenFlow Switches
        s1 = self.addSwitch('s1', protocols='OpenFlow13', failMode='secure')
        s2 = self.addSwitch('s2', protocols='OpenFlow13', failMode='secure')
        s3 = self.addSwitch('s3', protocols='OpenFlow13', failMode='secure')
        s4 = self.addSwitch('s4', protocols='OpenFlow13', failMode='secure')

        # 3. Add Host Links
        self.addLink(h1, s1)
        self.addLink(h2, s4)

        # 4. Add Inter-Switch Links
        # Primary Path: s1 -> s2 -> s4 (Fast: 5ms delay)
        self.addLink(s1, s2, cls=TCLink, bw=10, delay='5ms')
        self.addLink(s2, s4, cls=TCLink, bw=10, delay='5ms')

        # Backup Path: s1 -> s3 -> s4 (Backup: 20ms delay)
        self.addLink(s1, s3, cls=TCLink, bw=10, delay='20ms')
        self.addLink(s3, s4, cls=TCLink, bw=10, delay='20ms')

def run():
    topo = MultiPathTopo()
    # Runs standalone with Open vSwitch flow table management
    net = Mininet(
        topo=topo,
        switch=OVSSwitch,
        controller=None,
        autoSetMacs=True,
        autoStaticArp=True
    )
    
    info('*** Starting Network\n')
    net.start()
    
    info('*** Network Ready. Entering Mininet CLI\n')
    CLI(net)
    
    info('*** Stopping Network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
