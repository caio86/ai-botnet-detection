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

    # 1. Encontra automaticamente a interface correta no s1 que vai para o ids
    # connectionsTo retorna uma lista de tuplas: (interface_no_s1, interface_no_ids)
    interface_s1_para_ids = s1.connectionsTo(ids)[0][0]
    nome_da_porta = interface_s1_para_ids.name # Retornará algo como 's1-eth8'

    print(f"Configurando espelhamento de tráfego para a interface: {nome_da_porta}")

    ids_host_port = ids.defaultIntf().name

    cmd_mirror = (
        f"ovs-vsctl -- set Bridge s1 mirrors=@m "
        f"-- --id=@outport get Port {nome_da_porta} "
        f"-- --id=@m create Mirror name=ids-mirror select_all=true output-port=@outport"
    )

    result = s1.cmd(cmd_mirror)
    if result.strip():
        info(f" OVS Mirror Output: {result}\n")

    # CRITICAL: Put the IDS host interface into promiscuous mode so it doesn't drop the mirrored packets
    ids.cmd(f"ip link set {ids_host_port} promisc on")

    info(f"*** ***TESTE: {s1.intfList()}")

    info("*** Running CLI - Ready for Simulation ***\n")
    CLI(net)

    info("*** Stopping Network ***\n")
    net.stop()

if __name__ == "__main__":
    # Set the log level to info to see Mininet output
    setLogLevel("info")
    run()
