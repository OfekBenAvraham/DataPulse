declare module 'bencode' {
    const bencode: {
      encode: (data: any) => Buffer;
      decode: (data: Buffer | Uint8Array, encoding?: string) => any;
    };
    export default bencode;
  }
  