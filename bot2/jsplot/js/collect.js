
function Collector(revnos)
{
    this.plotdata = [];
    this.counter = revnos.length;

    this.finish_collecting = function() {
        this.plotdata = extract_benchmark_data(this.plotdata);
        var benchnames = _.keys(this.plotdata.results);
        benchnames.sort()
        for (var i = 0; i < benchnames.length; ++i) {
            var benchname = benchnames[i];
            var benchresults = this.plotdata.results[benchname];
            var cpystart = benchresults[0][0];
            var cpyend = benchresults[benchresults.length - 1][0];
            var cpyval = this.plotdata.cpytimes[benchname];
            var cpython_results = [[cpystart, cpyval], [cpyend, cpyval]]
            this.plot(benchname, benchresults, cpython_results,
                      this.plotdata.lasttimes[benchname])
        }
    }

    this.collect = function(next) {
        this.plotdata.push(next);
        this.counter--;
        if (this.counter == 0) {
            this.finish_collecting()
        }
    }
}

function collect_data(plot_function, revlist_url, base_url, async)
{
    $.ajax({
        url: revlist_url,
        dataType: 'html',
        success: function(htmlstr) {
            var revnos = extract_revnos($(htmlstr));
            var collector = new Collector(revnos);
            collector.plot = plot_function;
            for (var i in revnos) {
                $.ajax({
                    url: base_url + revnos[i] + '.json',
                    success: function(data) {
                    collector.collect(data)
                    },
                    dataType: 'json',
                    async: async,
                });
            }
        },
        async: async,
    });
}

function extract_benchmark_data(data)
{
    var retval = {};
    var cpytimes = {};
    var lasttimes = {}
    var lastrev = 0;
    var lastrevindex = 0;
    for (var i = 0; i < data.length; i++) {
        var revno = data[i]["revision"];
        if (revno > lastrev) {
            lastrev = revno;
            lastrevindex = i;
        }
        var results = data[i]["results"];
        for (var j = 0; j < results.length; j++) {
            var result = results[j];
            var name = result[0];
            var dataelem = result[2];
            var avg;
            if (dataelem["avg_changed"]) {
                avg = dataelem["avg_changed"];
            } else {
                avg = dataelem["changed_time"];
            }
            if (retval[name]) {
                retval[name].push([revno, avg]);
            } else {
                retval[name] = [[revno, avg]];
            }
        }
    }
    for (var name in retval) {
        retval[name].sort(function (a, b) {
            if (a[0] > b[0]) {
                return 1;
            } else {
                return -1;
            }
        });
    }
    var cpyelem = data[lastrevindex]
    for (var i = 0; i < cpyelem.results.length; i++) {
        var dataelem = cpyelem.results[i][2];
        var benchname = cpyelem.results[i][0];
        if (dataelem.avg_base) {
            cpytimes[benchname] = dataelem.avg_base;
            lasttimes[benchname] = dataelem.delta_avg;
        } else {
            cpytimes[benchname] = dataelem.base_time;
            lasttimes[benchname] = dataelem.time_delta;
        }
    }
    return {'results': retval, 'cpytimes': cpytimes,
            'lasttimes': lasttimes};
}

function extract_revnos(xmldoc)
{
    var res = [];
    $(xmldoc).find("a").each(function (no, elem) {
        var s = elem.getAttribute("href");
        s = s.substr(0, s.length - ".json".length);
        res.push(s);
    });
    return res;
}