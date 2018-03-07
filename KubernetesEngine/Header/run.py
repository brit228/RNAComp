import time

from google.cloud import datastore

import kubernetes.client
import kubernetes.config

def main():
    kubernetes.config.load_incluster_config()
    batchclient = kubernetes.client.BatchV1Api()
    ds = datastore.Client(project='rnacompute')
    while True:
        jobs = batchclient.list_namespaced_job('default').items
        for job in jobs:
            key = ds.key('jobs', int(job.metadata.name[4:]))
            if job.status.succeeded > 0:
                entity = ds.get(key)
                batchclient.delete_namespaced_job(job.metadata.name, 'default', kubernetes.client.V1DeleteOptions(propagation_policy='Foreground'))
                entity['Status'] = u"completed"
                ds.put(entity)
            if job.status.failed > 0:
                entity = ds.get(key)
                batchclient.delete_namespaced_job(job.metadata.name, 'default', kubernetes.client.V1DeleteOptions(propagation_policy='Foreground'))
                entity['Status'] = u"failed"
                ds.put(entity)
        query = ds.query(kind='jobs')
        query.add_filter('Status', '=', 'pending')
        query.order = ['TimeDate']
        querylist = list(query.fetch(limit=5))
        while len(jobs)<5 and len(querylist)>0:
            body = createJobTemplate(querylist[0])
            batchclient.create_namespaced_job('default', body)
            querylist[0]['Status'] = u"running"
            ds.put(querylist[0])
            del querylist[0]
        time.sleep(60)

def createJobTemplate(query):
    container = kubernetes.client.V1Container(name=query['Image'])
    container.image = 'us.gcr.io/rnacompute/jobs/'+query['Image']

    template = kubernetes.client.V1PodTemplateSpec()
    template.metadata = kubernetes.client.V1ObjectMeta()
    template.metadata.name = 'pod-' + str(query.key.id) + '-' + query['Name']
    template.spec = kubernetes.client.V1PodSpec(containers=[container])
    template.spec.restart_policy = "Never"

    body = kubernetes.client.V1Job()
    body.metadata = kubernetes.client.V1ObjectMeta()
    body.metadata.name = 'job-' + str(query.key.id)
    body.spec = kubernetes.client.V1JobSpec(template=template)
    body.spec.active_deadline_seconds = query['Walltime']
    body.spec.completions = 1
    body.spec.parallelism = 1
    return body

if __name__ == '__main__':
    main()
