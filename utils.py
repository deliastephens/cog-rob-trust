import IPython
from nose.tools import assert_equal, ok_
import numpy as np

from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from IPython.display import display, HTML, clear_output, display_html, Javascript
from pyperplan import planner

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

def run_pyperplan(domain_file, problem_file, search_type='astar', heuristic='hff'):
  """
  @param domain_file:    a string to the relative path of the domain pddl file (e.g., pddl/robot-domain.pddl)
  @param problem_file:   a string to the relative path of the problem file
  @param search_type:    a string from {'astar', 'wastar', 'gbf', 'bfs', 'ehs', 'ids', 'sat'}
  @param heuristic       a string from {'hff', 'hadd', 'hmax'} (there may be more; check out the Pyperplan documentation)

  @return solution       a list of actions that solve the problem 
  """
  search_alg = planner.SEARCHES[search_type]
  heuristic =  planner.HEURISTICS[heuristic]

  return planner.search_plan(domain_file, problem_file, search_alg, heuristic)

def test_ok():
    """ If execution gets to this point, print out a happy message """
    try:
        from IPython.display import display_html
        display_html("""<div class="alert alert-success">
        <strong>Tests passed!!</strong>
        </div>""", raw=True)
    except:
        print("Tests passed!!")

def check_omega(func):
    assert_equal(np.allclose(func(np.array([0, 0.3, 0.6, 1.0])), np.array([1., 0.7, 0.4, 0.])), True)
    assert_equal(np.allclose(func(np.array([0, 0.5, 1.0])), np.array([1., 0.5, 0. ])), True)
    assert_equal(np.allclose(func(np.array([0, 0.25, 0.5, 0.75, 1.0])), np.array([1., 0.75, 0.5, 0.25, 0.])), True)

def check_explicability_score(func):
    # same cost
    optimal, expected = 3, 3
    result = np.zeros((1,2))
    assert_equal(np.all(func(optimal, expected) == result), True)

    optimal, expected = 2,6
    result = np.array([0, -4])
    assert_equal(np.allclose(func(optimal, expected), result), True)

    optimal, expected = 4, 3
    result = np.array([0, 1])
    assert_equal(np.all(func(optimal, expected) == result), True)

def check_matrix(func):
    T = np.array([0, 0.3, 0.6, 1.0])
    w = np.array([1., 0.7, 0.4, 0.])
    E = np.array([0., -1.])
    P = np.array([[[1.,  0.,  0.,  0. ],
  [0.,  0.7, 0.3, 0. ],
  [0.,  0.,  0.4, 0.6],
  [0.,  0.,  0.,  1. ]],

 [[0.,  1.,  0.,  0. ],
  [0.,  0.,  1.,  0. ],
  [0.,  0.,  0.,  1. ],
  [0.,  0.,  0.,  1. ]]])
    assert_equal(np.allclose(func(T, w, E), P), True)
    
    T = np.array([0, 0.5, 0.7, 1.0])
    w = np.array([1., 0.5, 0.3, 0.])
    E = np.array([0, -4.])
    P = np.array([[[1.,  0.,  0.,  0. ],
  [0.,  0.5, 0.5, 0. ],
  [0.,  0.,  0.3, 0.7],
  [0.,  0.,  0.,  1. ]],

 [[0.,  1.,  0.,  0. ],
  [0.,  0.,  1.,  0. ],
  [0.,  0.,  0.,  1. ],
  [0.,  0.,  0.,  1. ]]])
    assert_equal(np.allclose(func(T, w, E), P), True)

def check_cost(func):
    w = np.array([1., 0.7, 0.4, 0.])
    E = np.array([0, 0])
    expected_cost = 3
    C = np.array([[0., 0.],
                 [0.9, 0.9],
                 [1.8, 1.8],
                 [3., 3.]])
    assert_equal(np.allclose(func(w, E, expected_cost), C), True)
    
    w = np.array([1., 0.5, 0.3, 0.])
    E = np.array([2, 4])
    expected_cost = 6
    C = np.array([[0., 0.],
                 [3., 3.],
                 [4.2, 4.2],
                 [6., 6.]])
    assert_equal(np.allclose(func(w, E, expected_cost), C), True)
    
def check_MDP(func):
    pass


def prep_browser():
    display(Javascript(JS))

num_divs = 0

def viz_plan(plan):
  global num_divs

  if len(plan) == 0:
      display_html("""<div class="alert alert-error">
      <strong>Planning failed!</strong>
      </div>""", raw=True)

  if plan:
      num_divs += 1
      display_html("""<div class="alert alert-success">
      <strong>Plan found!</strong>
      </div>""", raw=True)
      display_html('<div id="timeline-graph-' + str(num_divs) + '"></div>',
                    raw=True)
      # Create a plan string with action of 1 for every Operator in the solution
      plan_string = ''
      t = 0.0
      for op in plan:
        start_time = str(t) +': '
        action = str(op.name)
        duration = ' [1.0]\\n'
        plan_string += start_time + action + duration
        t += 1
      display_html('<script> window.display_timeline("timeline-graph-' + str(num_divs) + '", "' + plan_string + '") </script>',
                    raw=True)
  display_html("<strong>raw planner output:</strong>", raw=True)

  for action in plan:
    print(action.name)


def run_and_viz_pyperplan(domain_file, problem_file, search_type='astar', heuristic='hff'):
  solution = run_pyperplan(domain_file, problem_file, search_type, heuristic)
  global num_divs
    
  viz_plan(solution)

  if not solution:
      raise RuntimeError('Planning failed.')