export function trunc(str:string, n:number):string {
    if (str.length <= n) return str;
    return str.substr(0, n - 3) + '...';
}