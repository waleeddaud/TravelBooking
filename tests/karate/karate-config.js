function fn() {
  var config = {
    baseUrl: karate.properties['api.baseUrl'] || 'http://localhost:8000',
    authToken: null,
    userEmail: null
  };
  
  karate.configure('connectTimeout', 10000);
  karate.configure('readTimeout', 10000);
  
  return config;
}
