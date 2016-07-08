import boto3
import datetime
import sys
import re

client = boto3.client('codedeploy')

apps =  client.list_applications()

def getDeploymentGroups(app):
    return client.list_deployment_groups(applicationName=app)

def hasPaginate(deployments):
    if 'nextToken' in deployments:
        return True
    return False

def getCountWithPaginate(app,deploymentGroup,nextToken):
    deployments = client.list_deployments(applicationName=app,deploymentGroupName=deploymentGroup,
    createTimeRange={'start': datetime.datetime(int(sys.argv[1]),int(sys.argv[2]), int(sys.argv[3])),'end': datetime.datetime(int(sys.argv[4]),int(sys.argv[5]), int(sys.argv[6]))},
    nextToken=nextToken)
    return len(deployments['deployments'])

def getDeployments(app,deploymentGroup):
    deployments = client.list_deployments(applicationName=app,deploymentGroupName=deploymentGroup,
    createTimeRange={'start': datetime.datetime(int(sys.argv[1]),int(sys.argv[2]), int(sys.argv[3])),'end': datetime.datetime(int(sys.argv[4]),int(sys.argv[5]), int(sys.argv[6]))})
    paginate = 1;
    count = len(deployments['deployments'])
    while (True):
        try:
            deployments = client.list_deployments(applicationName=app,deploymentGroupName=deploymentGroup,
            createTimeRange={'start': datetime.datetime(int(sys.argv[1]),int(sys.argv[2]), int(sys.argv[3])),'end': datetime.datetime(int(sys.argv[4]),int(sys.argv[5]), int(sys.argv[6]))},
            nextToken=deployments['nextToken'])
            count = count + len(deployments['deployments'])
        except KeyError:
            break
    return count

for app in apps['applications']:
    deploymentGroups = getDeploymentGroups(app)
    for deploymentGroup in deploymentGroups['deploymentGroups']:
        Countdeployments = getDeployments(app,deploymentGroup)
        print deploymentGroup
        print Countdeployments
