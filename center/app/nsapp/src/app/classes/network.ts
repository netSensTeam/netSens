interface NetworkOverview {
    uuid:string;
    name:string;
    createTime:number;
    lastUpdateTime:number;
    defaultGTWMAC:string;
    deviceCout:number;
    linkCount:number;
    packetCount:number;
}

export  { NetworkOverview };