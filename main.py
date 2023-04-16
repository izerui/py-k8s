from k8s import K8sDeployment

if __name__ == '__main__':
    deployment = K8sDeployment()
    deployment.kill_invalid('test')
