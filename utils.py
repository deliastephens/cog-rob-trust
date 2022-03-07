from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
import re
from IPython.display import display, HTML, clear_output, display_html, Javascript

JS="""
require("notebook/js/outputarea").OutputArea.prototype._should_scroll = function(lines) {
    return false;
}

var tinycolor;

require.config({
  paths: {
      sha1: 'http://editor.planning.domains/plugins/featured/timeline-viewer/sha1.js',
      charts: 'https://www.gstatic.com/charts/loader.js'
  }
});

requirejs(['https://www.gstatic.com/charts/loader.js'],
          function() {
              google.charts.load('current', {packages: ['timeline']});
         });

requirejs(['https://courses.csail.mit.edu/16.410/js/sha1.js'],
          function() {
              console.log('Loaded SHA1');
         });

requirejs(['https://courses.csail.mit.edu/16.410/js/tinycolor.js'],
          function(m) {
              console.log('Loaded tinycolor');
              tinycolor = m;
         });

function get_terms(pred) {
  // Cut off the first and last characters - the parenthesis
  pred = pred.trim().slice(1, pred.length - 1);
  var words = pred.split(" ");
  return words;
}

function wordToColor(word, sat, lightness) {
  // Helper function that converts a word to a color based on the SHA1 sum
  var sha1_word = CryptoJS.SHA1(word).words[0];
  sha1_word = sha1_word % 360;
  if (sha1_word < 0) {
    sha1_word += 360;
  }
  var hsl_string = 'hsl(' + sha1_word + ", " + (100 * sat) + "%, " + (100 * lightness) + "%)";
  return '#' + tinycolor(hsl_string).toHex();
}

function activity_to_table_row(match, id) {
  var start_time = 1000*parseFloat(match[1]);
  var end_time = 1000*parseFloat(match[3]) + start_time;
  return ["" + id, match[2],  start_time, end_time];
}

function activity_to_color(match) {
  var words = get_terms(match[2]);
  var action_name = words[0].trim();
  var color = wordToColor(action_name, 0.7, 0.75);
  return color;
}

function display_timeline(chart_div, plan_string) {
    requirejs(['https://www.gstatic.com/charts/loader.js'],
        function() {
            google.charts.load('current', {packages: ['timeline']});
            google.charts.setOnLoadCallback(function () {display_timeline_cb(chart_div, plan_string)});
        });
}

window.display_timeline = display_timeline;

function display_timeline_cb(div_name, plan_string){
    // Add the google chart
    var options = {
      height: 100,
      animation: {
        duration: 1000,
        easing: 'out',
      },
      hAxis: {
        gridlines: {count: 15}
      },
      timeline: {
        showRowLabels: true,
        groupByRowLabel: false,
        colorByRowLabel: false,
      }
    };
    var chart = new google.visualization.Timeline(document.getElementById(div_name));
    
    // Get planner text
    var planner_output = plan_string;
    // Find all matches for lines that appear to be temporal actions
    var regexp = /^([\d.]+)\s*:\s*(\(.*\))\s*\[([\d.]+)\]$/gm;
    var matches = [];
    var match;
    while ((match = regexp.exec(planner_output)) !== null) {
      matches.push(match);
    }

    // Load the data into a table
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Task ID');
    data.addColumn('string', 'Task Name');
    data.addColumn('number', 'Start');
    data.addColumn('number', 'End');
    data.addRows([]);
    var colors_for_activities = [];
    for(var i = 0; i < matches.length; i++) {
        var match = matches[i];
        data.addRows([activity_to_table_row(match, i)])
        var color = activity_to_color(match)
        colors_for_activities.push(color);
    }

    // Draw the chart!
    options.height = data.getNumberOfRows() * 43 + 100;
    options.colors = colors_for_activities;
    chart.draw(data, options);
}
"""

def prep_browser():
    display(Javascript(JS))

num_divs = 0

class OpticParser():
    def __init__(self, optic_output):
        self.optic_output = optic_output

    def parse(self):
        # Parse with a regular expression, capturing the initial time, action, and duration
        expr = re.compile(r'^(\d+\.\d+):\s*(.*)\[(\d+\.\d+)\]$', re.MULTILINE)
        matches = expr.findall(self.optic_output)
        return [m[0] + ': ' + m[1].strip() + ' [' + m[2] + ']' for m in matches]

    def solution_found(self):
        return ';;;; Solution Found' in self.optic_output

def run_optic(domain, problem, timeout=None):
    if timeout:
        p = Popen(['optic-clp', domain, problem], stdout=PIPE, stderr=STDOUT)
    else:
        p = Popen(['optic-clp', '-N', domain, problem], stdout=PIPE, stderr=STDOUT)
    try:
        out, _ = p.communicate(timeout=timeout)
    except TimeoutExpired:
        p.kill()
        out, _ = p.communicate()
    code = p.returncode
    out = out.decode("utf-8") 
    return code, out

def run_and_viz_optic(domain_file, problem_file, timeout=None):
    global num_divs
    code, out = run_optic(domain_file, problem_file, timeout=timeout)
    parser = OpticParser(out)
    success = code == 0 and parser.solution_found()
    if timeout:
        display_html("<strong>raw planner output:</strong>", raw=True)
        for l in out.split("\n"):
            print(l)
        print("done")
        return
    
    if not success:
        display_html("""<div class="alert alert-error">
        <strong>Planning failed!</strong>
        </div>""", raw=True)
    else:
        num_divs += 1
        display_html("""<div class="alert alert-success">
        <strong>Plan found!</strong>
        </div>""", raw=True)
        display_html('<div id="timeline-graph-' + str(num_divs) + '"></div>',
                     raw=True)
        lines = parser.parse()
        plan_string = '\\n'.join(lines)
        display_html('<script> window.display_timeline("timeline-graph-' + str(num_divs) + '", "' + plan_string + '") </script>',
                     raw=True)
    display_html("<strong>raw planner output:</strong>", raw=True)
    for l in out.split("\n"):
        print(l)
    if not success:
        raise RuntimeError('Planning failed.')