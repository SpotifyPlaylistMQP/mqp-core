var http = require('http')
    , fs = require('fs')
    , url = require('url')
    , port = 8088;

var server = http.createServer(function (req, res) {
    var uri = url.parse(req.url)
    switch (uri.pathname) {
        // - - - - - HTML Cases - - - - -
        case '/':
            sendFile(res, 'public/index.html')
            break
        case '/index.html':
            sendFile(res, 'public/index.html')
            break
        // - - - - - CSS Cases - - - - -
        case '/css/bootstrap.css':
            sendFile(res, 'public/css/bootstrap.css', 'text/css')
            break
        case '/css/style.css':
            sendFile(res, 'public/css/style.css', 'text/css')
            break
        case '/css/datavis.css':
            sendFile(res, 'public/css/datavis.css', 'text/css')
            break
        case '/css/bootstrap.min.css.map':
            sendFile(res, 'public/css/bootstrap.min.css.map', 'text/javascript')
            break
        case '/css/spot.png':
            sendFile(res, 'public/css/spot.png', 'image/png')
            break
        // - - - - - JS Cases - - - - -
        /*
            Section 1: D3 JS files
        */
        case '/js/d3/graphMaster.js':
            sendFile(res, 'public/js/d3/graphMaster.js', 'text/js')
            break
        case '/js/d3/radar_graph.js':
            sendFile(res, 'public/js/d3/radar_graph.js', 'text/javascript')
            break
        case '/js/d3/line_graph.js':
            sendFile(res, 'public/js/d3/line_graph.js', 'text/javascript')
            break
        case '/js/d3/table.js':
            sendFile(res, 'public/js/d3/table.js', 'text/javascript')
            break
        /*
            Section 2: Other JS files
        */
        case '/js/bootstrap.js':
            sendFile(res, 'public/js/bootstrap.js', 'text/javascript')
            break
        case '/js/popper.js':
            sendFile(res, 'public/js/popper.js', 'text/javascript')
            break
        case '/js/popper.min.js.map':
            sendFile(res, 'public/js/popper.min.js.map', 'text/javascript')
            break
        case '/js/bootstrap.min.js.map':
            sendFile(res, 'public/js/bootstrap.min.js.map', 'text/javascript')
            break
        // - - - - - Data Cases - - - - -
        case '/data/mf_mpd_square_100':
            sendFile(res, 'public/data/mf_mpd_square_100', 'text')
            break
        case '/data/feature_mf_mpd_square_100':
            sendFile(res, 'public/data/feature_mf_mpd_square_100', 'text')
            break
        case '/data/playlist_average.json':
            sendFile(res, 'public/data/playlist_average.json', 'application/json; charset=UTF8')
            break
        case '/data/song_average.json':
            sendFile(res, 'public/data/song_average.json', 'application/json; charset=UTF8')
            break
        case '/data/dataset_average.json':
            sendFile(res, 'public/data/dataset_average.json', 'application/json; charset=UTF8')
            break
        // - - - - - Data Cases - - - - -
        case '/css/cocogoose-classic-medium-trial-webfont.woff':
            sendFile(res, 'public/css/fonts/cocogoose-classic-medium-trial-webfont.woff', 'text')
            break
        case '/css/cocogoose-classic-medium-trial-webfont.woff2':
            sendFile(res, 'public/css/fonts/cocogoose-classic-medium-trial-webfont.woff2', 'text')
            break
        // - - - - - Default Cases - - - - -
        default:
            console.log('Error 404 ' + uri.pathname + " not found!")
            res.end('404 not found')
    }
})

server.listen(process.env.PORT || port);
console.log('listening on 8080')

function sendFile(res, filename, contentType) {
    contentType = contentType || 'text/html';

    fs.readFile(filename, function (error, content) {
        res.writeHead(200, {'Content-type': contentType})
        res.end(content, 'utf-8')
    })

}
