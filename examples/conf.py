import multiprocessing

bind = ['127.0.0.1:9090']
workers = multiprocessing.cpu_count()
worker_class = 'thrift_gevent'

thrift_transport_factory = 'thrift.transport.TTransport:TBufferedTransportFactory'
thrift_protocol_factory = 'thrift.protocol.TCompactProtocol:TCompactProtocolFactory'
service_register_cls = 'gunicorn_thrift.register:ZookeeperRegister'
service_register_conf = {
    'addr' : '127.0.0.1:2181',
    'path' : '/test/gunicorn-thrift/server'
}

# Server Hooks
def on_exit(server):
    service_watcher = server.app.service_watcher
    if service_watcher:
        instances = []
        for i in server.cfg.address:
            port = i[1]
            instances.append({'port': {"main": port},
                              'meta': None,
                              'state': 'up'})
        service_watcher.remove_instance(instances)

