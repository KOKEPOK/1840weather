var PROTO_PATH = __dirname + '/../protos/GreetingService.proto';

var grpc = require('@grpc/grpc-js');
var protoLoader = require('@grpc/proto-loader');
var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });
var Greeting_proto = grpc.loadPackageDefinition(packageDefinition).name_package;

/**
 * Implements the SayHello RPC method.
 */
function sayHello(call, callback) {
  class HashTable {
  constructor() {
    this.table = new Array(127);
    this.size = 0;
  }

  _hash(key) {
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
      hash += key.charCodeAt(i);
    }
    return hash % this.table.length;
  }

  set(key, value) {
    const index = this._hash(key);
    if (this.table[index]) {
      for (let i = 0; i < this.table[index].length; i++) {
        if (this.table[index][i][0] === key) {
          this.table[index][i][1] = value;
          return;
        }
      }
      this.table[index].push([key, value]);
    } else {
      this.table[index] = [];
      this.table[index].push([key, value]);
    }
    this.size++;
  }

  get(key) {
    const index = this._hash(key);
    if (this.table[index]) {
      for (let i = 0; i < this.table.length; i++) {
        if (this.table[index][i][0] === key) {
          return 'True';
        }
      }
    }
    return 'False';
  }
}
const ht = new HashTable();
ht.set("Oleg", "Kovynev");
ht.set("Alex", "Lukyanchenko");
ht.set("Andrey", "Ivanov");
if (ht.get(call.request.name)) {
  return callback(null, {message:ht.get(call.request.name)});}
}

/**
 * Starts an RPC server that receives requests for the Greeter service at the
 * sample server port
 */
function main() {
  var server = new grpc.Server();
  server.addService(Greeting_proto.Greeter.service, {sayHello: sayHello});
  server.bindAsync('0.0.0.0:50052', grpc.ServerCredentials.createInsecure(), () => {
    server.start();
  });
}

main();

