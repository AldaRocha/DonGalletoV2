jQuery.extend(jQuery.fn.dataTable.ext.oSort, {
    "date-pre": function (a) {
        if (a == null || a == "") {
            return 0;
        }
        var ukDatea = a.split('/');
        return (ukDatea[2] + ukDatea[1] + ukDatea[0]) * 1;
    },

    "date-asc": function (a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "date-desc": function (a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    },
    
    
    "time-pre": function (a) {
        var uniTime;

        if (a.toLowerCase().indexOf("am") > -1 || (a.toLowerCase().indexOf("pm") > -1 && Number(a.split(":")[0]) === 12)) {
            uniTime = a.toLowerCase().split("pm")[0].split("am")[0];
            while (uniTime.indexOf(":") > -1) {
                uniTime = uniTime.replace(":", "");
            }
        } else if (a.toLowerCase().indexOf("pm") > -1 || (a.toLowerCase().indexOf("am") > -1 && Number(a.split(":")[0]) === 12)) {
            uniTime = Number(a.split(":")[0]) + 12;
            var leftTime = a.toLowerCase().split("pm")[0].split("am")[0].split(":");
            for (var i = 1; i < leftTime.length; i++) {
                uniTime = uniTime + leftTime[i].trim().toString();
            }
        } else {
            uniTime = a.replace(":", "");
            while (uniTime.indexOf(":") > -1) {
                uniTime = uniTime.replace(":", "");
            }
        }
        return Number(uniTime);
    },

    "time-asc": function (a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "time-desc": function (a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    },
    
    
    "datetime-pre": function ( a ) {
        var x;
 
        if ( $.trim(a) !== '' ) {
            var frDatea = $.trim(a).split(' ');
            var frTimea = (undefined != frDatea[1]) ? frDatea[1].split(':') : [00,00,00];
            var frDatea2 = frDatea[0].split('/');
            x = (frDatea2[2] + frDatea2[1] + frDatea2[0] + frTimea[0] + frTimea[1] + ((undefined != frTimea[2]) ? frTimea[2] : 0)) * 1;
        }
        else {
            x = Infinity;
        }
 
        return x;
    },
 
    "datetime-asc": function ( a, b ) {
        return a - b;
    },
 
    "datetime-desc": function ( a, b ) {
        return b - a;
    }
});