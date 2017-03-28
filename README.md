# [Luigi](http://luigi.readthedocs.io/en/stable/configuration.html)

#### 1.install luigi        
pip install luigi

#### 2.set config       
~ config location     
1. /etc/luigi/client.cfg
2. luigi.cfg (or legacy name client.cfg) in your current working directory
3. LUIGI_CONFIG_PATH environment variable


~ client.cfg

[hdfs]      
client: hadoopcli       
snakebite_autoconfig: false     
namenode_host: localhost        
namenode_port: 50030        

[hadoop]        
version: cdh4       
streaming-jar: /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce/hadoop-streaming.jar      

[core]      
default-scheduler-host: 0.0.0.0     
logging_conf_file: test/testconfig/logging.cfg      


#### 3.run luigi sever      
1. python /usr/local/lib/python2.7/site-packages/luigi/server.py
2. luigid &
check ==> http://localhost:8082/static/visualiser/index.html
