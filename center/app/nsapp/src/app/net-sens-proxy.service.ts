import { Injectable } from '@angular/core';
// import { Network } from './classes/network';
import { HttpClient } from '@angular/common/http';
import { NetworkOverview } from './classes/network'
@Injectable({
  providedIn: 'root'
})
export class NetSensProxyService {
  connected:boolean;
  loggedIn:boolean;
  loginName:string;

  constructor(private http: HttpClient) { 
    this.connected = false;
    this.loggedIn = true;
    this.loginName = 'dummy';
  }

  getNetwork(uuid:string):NetworkOverview {
    return null;
  }

  getNetworks(filter:any=null) {
    // if (!this.loggedIn) return callback("User not logged in");
    // let net = new Network({
    //   uuid: 'blabla',
    //   name: 'yossi',
    //   createTime: (new Date()).getTime()/1000-100,
    //   lastUpdateTime: (new Date()).getTime()/1000,
    //   defaultGTWMAC: 'AA:AA:AA:AA:AA:AA',
    //   deviceCount: 10,
    //   linkCount: 5,
    //   packetCount: 1000
    // });
    // callback(null, [net]);
    return this.http.get('http://localhost:8000/api/overview', { observe: 'response' });
  }

  renameNetwork(networkId:string, newName:string){
    console.log('Renaming network');
    this.http.post('http://localhost:8000/api/networks/' + networkId + '/rename',
                    {name: newName}, {observe: 'response'}).subscribe(() => {
                      console.log('Rename posted');
                    });
  }

  deleteNetwork(networkId:string) {
    console.log('Deleting network');
    this.http.delete('http://localhost:8000/api/networks/' + networkId).subscribe(
      () => {console.log('delete requested'); }
    )
  }
}
