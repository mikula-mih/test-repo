

# `REST` - REpresentational State Transfer;
#   the basic idea ia that when you want to take some action on a resource you
#   send an http request and the body of that request contains the desired new
#   state and the server will reply with the actual state sfter handling the
#   request;
# REST interfaces are therefore resource oriented;
# RPC (remote procedure calls) style interfaces are action oriented;

# REST issues:
#   - make sure yourself that REST interface adheres to the standard
#   - having to coordinate several requests in the front end to get the data you
#       need and waiting for request complition -> slows down UX
#   - REST doesn't enforce distinction between the structure of the data in the
#       database and the structure of the data that you recieve and send;
#       Leading to potential security issues
# use layered architecture, where you explicitly translate data from database
# into its public form;
#   - there is no way to control how much data you get back from request

# `GraphQL` -
# ReST has multiple endpoints and uses various http vers(GET,POST,...) to
# interact with the server;
# GraphQL uses a single endpoint and a query language; views the data as a graph
#   structure where objects are connected by relationships and thus forming a graph;

# GraphQL issues:
#   - sending a request to the server is more complicated, since you have to
#       specify the query or the invitation that you want to make; and with REST
#       that's just encoded in the endpoint and the http verb;
#   - suffers from the n+1 problem: if you retrieve a bunch of blogs with an author
#       a separate database request is going to be made for each offer and that
#       potentially slows things down; fixing by introducing some local caching
#       mechanism in the back end to avoid all those different database requests;
#   - not everything in graphql is standardized;
