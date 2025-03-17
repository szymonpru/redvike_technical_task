from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, ElastiCache, Database
from diagrams.aws.general import Users
from diagrams.aws.integration import SQS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.mobile import Mobile
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito, IAM, WAF
from diagrams.ibm.user import Browser
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Internet

# Create the diagram
with Diagram("Online Marketplace Architecture", show=False, direction="TB"):
    # Clients
    with Cluster("Clients"):
        web_clients = Browser("Web Clients")
        mobile_clients = Mobile("Mobile Clients")
        internet = Internet("Internet")

    # API Gateway and Security
    with Cluster("API Gateway & Security"):
        api_gateway = APIGateway("API Gateway")
        waf = WAF("AWS WAF")
        shield = WAF("AWS Shield")
        iam = IAM("AWS IAM")

    # Authentication & Authorization
    with Cluster("Authentication & Authorization"):
        cognito = Cognito("AWS Cognito")
        lambda_authorizer = Lambda("Lambda Authorizer")

    # Microservices
    with Cluster("Microservices"):
        user_service = Lambda("User Service")
        product_service = Lambda("Product Service")
        order_service = Lambda("Order Service")
        payment_service = Lambda("Payment Service")
        notification_service = Lambda("Notification Service")

    # Databases
    with Cluster("Databases"):
        rds = RDS("Amazon RDS (PostgreSQL)")
        dynamodb = Database("Amazon DynamoDB")
        redis = ElastiCache("Amazon ElastiCache (Redis)")

    # Message Queue
    with Cluster("Message Queue"):
        sqs = SQS("Amazon SQS")

    # Third-Party Integrations
    with Cluster("Third-Party Integrations"):
        payment_providers = Users("Third-Party Payment Providers")
        external_inventory = Users("External Inventory System")

    # Monitoring & Logging
    with Cluster("Monitoring & Logging"):
        cloudwatch = Cloudwatch("Amazon CloudWatch")
        xray = Prometheus("AWS X-Ray")

    # Connections
    web_clients >> internet >> api_gateway
    mobile_clients >> internet >> api_gateway

    api_gateway >> cognito
    api_gateway >> lambda_authorizer
    lambda_authorizer >> api_gateway

    api_gateway >> user_service
    api_gateway >> product_service
    api_gateway >> order_service
    api_gateway >> payment_service
    api_gateway >> notification_service

    user_service >> rds
    order_service >> rds
    product_service >> dynamodb
    product_service >> redis
    order_service >> redis

    order_service >> sqs
    product_service >> sqs
    sqs >> notification_service
    sqs >> external_inventory

    payment_service >> payment_providers

    # Monitoring & Logging
    user_service >> cloudwatch
    product_service >> cloudwatch
    order_service >> cloudwatch
    payment_service >> cloudwatch
    notification_service >> cloudwatch
    api_gateway >> cloudwatch
    lambda_authorizer >> cloudwatch

    user_service >> xray
    product_service >> xray
    order_service >> xray
    payment_service >> xray
    notification_service >> xray
    api_gateway >> xray
    lambda_authorizer >> xray

    # Security
    api_gateway >> waf
    api_gateway >> shield
    api_gateway >> iam
