import logging
import unittest
from typing import Callable

from kubernetes import client, config
from kubernetes.client import V1DeploymentList, V1Deployment


class TestTable(unittest.TestCase):

    def setUp(self):
        # Configs can be set in Configuration class directly or using helper utility
        config.load_kube_config()

    def test_pod(self):
        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    def test_deployment(self):
        namespace = 'test'
        v1 = client.AppsV1Api()
        apps: V1DeploymentList = v1.list_namespaced_deployment(namespace)
        for item in apps.items:
            try:
                app_name = item.metadata.name
                lang = item.spec.template.metadata.labels['language'] if item.spec.template.metadata.labels else None
                # app_name = item.metadata.labels['app'] if item.metadata.labels else None
                app_version = item.metadata.labels['version'] if item.metadata.labels else None
                status = 'False' not in list(
                    map(lambda x: x.status, item.status.conditions)) if item.status.conditions else True
                if lang and lang == 'java' and app_version == 'v1' and not status:
                    print(app_name, app_version, status)
                    patch_body = {"spec": {"replicas": 0}}
                    v1.patch_namespaced_deployment_scale(app_name, namespace, patch_body)
            except BaseException as e:
                logging.warn(e)

    def __catch_with_call(self, param, callParam: Callable, defaultVar):
        try:
            return callParam(param)
        except:
            return defaultVar
