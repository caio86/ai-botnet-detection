#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo


class BotnetTopo(Topo):
    """
    Custom topology for Botnet Simulation.
    Includes: Normal hosts, Bots, a C&C Server, and a Target Victim.
    """

    def build(self):
        # Add a central switch
        s1 = self.addSwitch("s1")

        # Add Normal/Benign Hosts
        h1 = self.addHost("h1", ip="10.0.0.1/24", mac="00:00:00:00:00:01")
        h2 = self.addHost("h2", ip="10.0.0.2/24", mac="00:00:00:00:00:02")

        # Add Bot Hosts (Zombies)
        bot1 = self.addHost("bot1", ip="10.0.0.11/24", mac="00:00:00:00:00:11")
        bot2 = self.addHost("bot2", ip="10.0.0.12/24", mac="00:00:00:00:00:12")
        bot3 = self.addHost("bot3", ip="10.0.0.13/24", mac="00:00:00:00:00:13")

        # Add Command & Control (C&C) Server
        cnc = self.addHost("cnc", ip="10.0.0.50/24", mac="00:00:00:00:00:50")

        # Add Target/Victim Server
        victim = self.addHost("victim", ip="10.0.0.100/24", mac="00:00:00:00:00:99")

        # Add IDS server with AI
        ids = self.addHost("ids", ip="10.0.0.254/24")

        # Connect all nodes to the central switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(bot1, s1)
        self.addLink(bot2, s1)
        self.addLink(bot3, s1)
        self.addLink(cnc, s1)
        self.addLink(victim, s1)
        self.addLink(ids, s1)

def run():
    topo = BotnetTopo()
    # Initialize the network with the custom topology
    net = Mininet(topo=topo, switch=OVSBridge, controller=None, waitConnected=True)

    info("*** Starting Network ***\n")
    net.start()

    info("*** Testing Basic Connectivity ***\n")
    net.pingAll()

    s1 = net.get('s1')
    ids = net.get('ids')

    s1.cmd('ovs-vsctl -- set Bridge s1 mirrors=@m '
       '-- --id=@m create Mirror name=ids-mirror '
       'select_all=1 output-port=' + s1.intf('s1-eth' + str(len(s1.intfList()))).name)

    info("*** Running CLI - Ready for Simulation ***\n")
    CLI(net)

    info("*** Stopping Network ***\n")
    net.stop()

if __name__ == "__main__":
    # Set the log level to info to see Mininet output
    setLogLevel("info")
    run()
