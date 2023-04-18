import logging

from kubernetes import config, client
from kubernetes.client import V1DeploymentList


class K8sDeployment:
    def __init__(self):
        super().__init__()
        config.load_kube_config()
        self.v1 = client.AppsV1Api()

    def kill_invalid(self, namespace):
        '''
        杀掉已经失效的pod,即将其Deployment的replicas设置为0
        :param namespace:
        :return:
        '''

        apps: V1DeploymentList = self.v1.list_namespaced_deployment(namespace)
        for item in apps.items:
            try:
                app_name = item.metadata.name
                lang = item.spec.template.metadata.labels['language'] if item.spec.template.metadata.labels else None
                # app_name = item.metadata.labels['app'] if item.metadata.labels else None
                app_version = item.metadata.labels['version'] if item.metadata.labels else None
                replicas = item.spec.replicas
                status = 'False' not in list(
                    map(lambda x: x.status, item.status.conditions)) if item.status.conditions else True
                if replicas > 0 and lang and lang == 'java' and app_version == 'v1' and not status:
                    # print(app_name, app_version, status)
                    patch_body = {"spec": {"replicas": 0}}
                    self.v1.patch_namespaced_deployment_scale(app_name, namespace, patch_body)
                    print(app_name, app_version, status, '已经将其replicas设置为0')
            except BaseException as e:
                logging.warn(app_name)

    def restart(self, namespace):
        '''
        重启后台服务
        :param namespace:
        :return:
        '''

        apps: V1DeploymentList = self.v1.list_namespaced_deployment(namespace)
        for item in apps.items:
            try:
                app_name = item.metadata.name
                lang = item.spec.template.metadata.labels['language'] if item.spec.template.metadata.labels else None
                # app_name = item.metadata.labels['app'] if item.metadata.labels else None
                app_version = item.metadata.labels['version'] if item.metadata.labels else None
                replicas = item.spec.replicas
                status = 'False' not in list(
                    map(lambda x: x.status, item.status.conditions)) if item.status.conditions else True
                if replicas > 0 and lang and lang == 'java' and app_version == 'v1':
                    # print(app_name, app_version, status)
                    patch_body = {"spec": {"replicas": 0}}
                    self.v1.patch_namespaced_deployment_scale(app_name, namespace, patch_body)
                    patch_body = {"spec": {"replicas": 1}}
                    self.v1.patch_namespaced_deployment_scale(app_name, namespace, patch_body)
                    print(app_name, app_version, status, '已经重启')
            except BaseException as e:
                logging.warn(app_name)