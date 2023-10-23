import radius as radius

@description('Specifies the environment for resources.')
param environment string

resource app 'Applications.Core/applications@2023-10-01-preview' = {
  name: 'raddemo'
  properties: {
    environment: environment
  }
}

resource redis 'Applications.Datastores/redisCaches@2023-10-01-preview' = {
  name: 'redis'
  properties: {
    application: app.id
    environment: environment
  }
}

resource gateway 'Applications.Core/gateways@2023-10-01-preview' = {
  name: 'gateway'
  properties: {
    application: app.id
    routes: [
      {
        path: '/'
        destination: 'http://ui:8001'
      }
    ]
  }
}


resource ui 'Applications.Core/containers@2023-10-01-preview' = {
  name: 'ui'
  properties: {
    application: app.id
    container: {
      image: 'gbaeke/radius-ui:latest'
      ports: {
        web: {
          containerPort: 8001
        }
      }
      env: {
        DAPR_APP: api.name  // api name is the same as the Dapr app id here
      }
    }
    extensions: [
      {
        kind: 'daprSidecar'
        appId: 'ui'
      }
    ]
  }
}

resource api 'Applications.Core/containers@2023-10-01-preview' = {
  name: 'api'
  properties: {
    application: app.id
    container: {
      image: 'gbaeke/radius-api:latest'
      ports: {
        web: {
          containerPort: 8000
        }
      }
      env: {
          REDIS_HOST: redis.properties.host
          REDIS_PORT: string(redis.properties.port)
      }
    }
    extensions: [
      {
        kind: 'daprSidecar'
        appId: 'api'
        appPort: 8000
      }
    ]
    connections: {
      redis: {
        source: redis.id  // this creates environment variables in the container
      }
    }
  }
}
