Be mindful if a codebase follows a different architecture or layer naming convention, and only apply these rules if applicable.

### General Overview

- Architect applications with four layers: API, Services, Domain, Infrastructure.
- API should depend only on Services.
- Services should depend only on Domain.
- Infrastructure should depend only on Domain.
- Domain should not depend on any other layer.
- A Utils "layer" (utility layer) should be created for cross-cutting concern code like
  Settings, etc. It should not depend on any other layer.
- All layers should be able to call on the Utils layer.
- Concrete infrastructure implementations should be injected via the "inject" library,
  which maps from interface classes (ABC) to concrete classes, either real ones or fake
  ones depending on a LOCAL_TESTING environment variable (this should be in Settings).

### API layer

- This layer should contain all code related to uvicorn, FastAPI, FastMCP or whichever
  server and backend library is being used, as well as authentication, authorization and
  data sanitization/validation in the endpoints.
- Leverage exception handlers whenever possible to catch custom application exceptions.
- Do not include business logic nor infrastructure/persistence/connection code here.
- Inject services from the Services layer.

### Services layer

- Services must be very thin classes that contain a cohesive group of use cases, like
  a class AuthService that deals with everything authorization/authentication related.
- A Service's methods should not be longer than 10-20 lines of code, otherwise either we
  need to extract logic to helper functions in separated files, or extract logic to
  the Domain or the Infrastructure layer depending on what type of logic it is.
- The Services layer must also contain the data structure classes to be used by the API
  layer to communicate with the services.

### Domain layer

- Here should fall all business logic and entities that are critical to the application.
- Code here does not need to be inside classes; pure functions are preferred, unless
  there is too much logic to handle and a class with multiple methods and attributes is
  needed.

### Infrastructure

- Infrastructure should contain all implementations to connect and handle operations on
  external systems like databases, application's APIs, etc.
- For each real implementation there should be a fake one that can be used for testing.
- If there is additional transformation of data needed to be made before persisting
  domain entities, and it doesn't add value to the application, it must be defined in
  the Infrastructure layer.

### In a nutshell

- The API layer must contain all API related code; it can only import code from Services
  and Utils.
- The Services layer must contain classes that encapsulate the application's behavior as
  well as the classes that act as contract for the data that it expects from the API. It
  should only import code form Domain and Utils.
- The Domain layer must contain all the business logic and entities, as well as the
  interfaces (ports) for persistence or communication with external services. It may only
  import code from Utils.
- The Infrastructure layer must contain all code related to persistence or communication
  with external services. It may import code from Domain and Utils.
- The Utils directory should not import code from anywhere in the codebase.
