module.exports = (req, res, next) => {
  const getRequestDataByMethod = method => {
    switch (method) {
      case "GET":
        return JSON.stringify(req.query);
      case "POST":
        return (
          Array.isArray(req.body)
            ? JSON.stringify({"numberOfItems": req.body.length})
            : JSON.stringify({"numberOfItems": 1})
        );
      default:
        return "The server does not know what to print for this HTTP method"
    }
  };

  const timestamp = new Date();
  console.log('%s-%s: %s %s %s',
    timestamp.toLocaleDateString(),
    timestamp.toLocaleTimeString(),
    req.method,
    req.originalUrl,
    getRequestDataByMethod(req.method)
  );
  next();
};