class envYamlConverter:
    
    def __init__(self, appName, namespace, secretsName, fileName, ipsName, image):
        self.appName = appName
        self.namespace = namespace
        self.image = image
        self.secretsName = secretsName
        self.fileName = fileName
        self.ipsName = ipsName
        return

    def convertToYaml(self, envList, secretsList):
        deploymentCode = (
            "# Deploy "+self.appName+"\n"
            "\n"
            "---\n"
            "apiVersion: apps/v1\n"
            "kind: Deployment\n"
            "metadata:\n"
            "  name: "+self.appName+"\n"
            "  namespace: "+self.namespace+"\n"
            "  labels:\n"
            "    app: "+self.appName+"\n"
            "spec:\n"
            "  replicas: 1\n"
            "  selector:\n"
            "    matchLabels:\n"
            "      app: "+self.appName+"\n"
            "  template:\n"
            "    metadata:\n"
            "      labels:\n"
            "        app: "+self.appName+"\n"
            "    spec:\n"
            "      containers:\n"
            "        - name: "+self.appName+"\n"
            "          image: "+self.image+"\n"
            "          imagePullPolicy: Always\n"
            "          env:\n"
        )
        f = open("deployment.yaml", "w")
        f.write(deploymentCode)
        for env in envList:
            env = env.replace(' ', '').split('=', 1)
            envName = env[0]
            envVal = env[1]
            if(envVal[0] == '"'):
                envVal = envVal[1:-1]
            f.write("            - name: "+envName+"\n")
            # Build yaml
            if envName not in secretsList:
                f.write("              value: "+'"'+envVal+'"\n')
            else:
                f.write("              valueFrom:\n")
                f.write("                secretKeyRef:\n")
                f.write("                  name: "+self.secretsName+"\n")
                f.write("                  key: "+envName.lower()+"\n")
        f.write("      imagePullSecrets:\n")
        f.write("        - name: "+self.ipsName+"\n")
        f.close()
        return

    def convertEnv(self, secretsList):
        #Store each line into a list
        envList = []
        with open(self.fileName, 'r+') as f:
            for line in f.readlines():
                lineToAppend = line.split("#", 1)[0].rstrip()
                if(lineToAppend != ''):
                    envList.append(lineToAppend)
        self.convertToYaml(envList, secretsList)