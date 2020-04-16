import { Component, OnInit } from '@angular/core';
import {NetSensProxyService} from '../net-sens-proxy.service';
import { NetworkOverview } from '../classes/network';
import { trunc } from '../utils/trunc';

@Component({
  selector: 'app-networks',
  templateUrl: './networks.component.html',
  styleUrls: ['./networks.component.scss']
})
export class NetworksComponent implements OnInit {
  networks:NetworkOverview[];

  constructor(private _proxy:NetSensProxyService) { 
  }

  ngOnInit(): void {
    setInterval( () => {
      this._proxy.getNetworks().subscribe(
        (response:any) => {
          this.networks = response.body.networks;
        }
      )
    }, 1000);
  }

  renameNetwork(network:NetworkOverview) {
    let newName = prompt('Select a new name:', network.name || network.uuid);
    if (newName === network.name) return;
    this._proxy.renameNetwork(network.uuid, newName);
  }

  loadNetwork(network:any) {

  }

  deleteNetwork(network:any) {

  }

  truncString(str:string):string {
    return trunc(str, 8);
  }
}
