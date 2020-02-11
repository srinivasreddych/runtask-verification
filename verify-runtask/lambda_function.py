import json
import os
import logging
import boto3
import sys
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Initializing clients
sns = boto3.client('sns')

def verify_runtask(event, context):
    #sns_arn=os.getenv(sns_arn)
    print (event)
    clusterName=event['detail']['requestParameters']['cluster']
    taskDef=event['detail']['requestParameters']['taskDefinition']
    eventTime=event['detail']['eventTime']

    try:
        if not event['detail']['responseElements'] and ((event['detail']['errorMessage'] or event['detail']['errorCode']) is not None): 
            print ("no responseElements detected but detected errorCode:{} and errorMessage:{}".format(event['detail']['errorMessage'], event['detail']['errorCode']))
            message="Task failed due to "+event['detail']['errorMessage']+" by raising an exception "+event['detail']['errorCode']+" on the ClusterName: "+clusterName+" launched by TaskDefinition: "+taskDef+" at TimeStamp: "+eventTime
            send_notification(message)
        elif not event['detail']['responseElements']['failures']:
            print ('no problems detected, seems like RunTask API call was successful')
            sys.exit(0)
        else: 
            reason=event['detail']['responseElements']['failures'][0]['reason']
            arn=event['detail']['responseElements']['failures'][0]['arn']
            print ("Reason for failing is {}".format(reason))
            print ("Reason for failing is {}".format(arn))
            message="Task failed due to "+reason+" on the ContainerInstanceArn: "+arn+" on the ClusterName: "+clusterName+" launched by TaskDefinition: "+taskDef+" at TimeStamp: "+eventTime
            send_notification(message)
    except KeyError:
        print ("KeyError detected")
    
        
def send_notification(message):
    response = sns.publish(
    TopicArn='arn:aws:sns:us-east-1:560360184571:dynamodb',   
    Message=message
    )
