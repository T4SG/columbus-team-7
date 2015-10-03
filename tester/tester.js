var alexa = require('alexa-app');
var app = new alexa.app('lebronjames');
 
app.intent('number',
  {
    "slots":{"text":"LITERAL"}
    ,"utterances":[ "{text}" ]
  },
  function(request,response) {
    var number = request.slot('text');
    response.say("Thanks for telling me your day was "+text);
  }
);
 
exports.handler = app.lambda();