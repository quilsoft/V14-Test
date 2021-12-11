odoo.define('project_scrum_portal.highchart_init_custom', function (require) {
"use strict";
    var core = require('web.core');
    var ajax = require('web.ajax');
    $(document).ready(function() {
    	
    	// Task Stage Column Chart
    	$('.task_stage_bar_btn').on('click', function(){
    	ajax.jsonRpc("/get_task_data", 'call', {
			'project_id': $('.task_id').val(),
		}).then(function(result) {
			Highcharts.chart('task_stage_bar_chart', {
			    chart: {
			        type: 'column'
			    },
			    title:false,
			    xAxis: {
			        categories: result.stages,
			        crosshair: true
			    },
			    yAxis: {
			        min: 0,
			        title: {
			            text: 'Number of Task(s)'
			        }
			    },
			    plotOptions: {
			        column: {
			            pointPadding: 0.2,
			            borderWidth: 0
			        }
			    },
			    credits: {
			        enabled: false
			    },
			    series: [{
			        name: 'No of Task',
			        data: result.stage_data

			    }]
			});
		});
    	});
		
		// Task Stage Pie Chart
    	$('.task_stage_pie_btn').on('click', function(){
		ajax.jsonRpc("/get_task_data", 'call', {
			'project_id': $('.task_id').val(),
		}).then(function(result) {
			Highcharts.chart('task_stage_pie_chart', {
			    chart: {
			        plotBackgroundColor: null,
			        plotBorderWidth: null,
			        plotShadow: false,
			        type: 'pie'
			    },
//			    title: {
//			        text: 'Browser market shares in January, 2018'
//			    },
//			    tooltip: {
//			        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
//			    },
			    accessibility: {
//			        point: {
//			            valueSuffix: '%'
//			        }
			    },
			    plotOptions: {
			        pie: {
			            allowPointSelect: true,
			            cursor: 'pointer',
			            dataLabels: {
			                enabled: false,
			                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
			            }
			        }
			    },
			    series: [{
			        name: 'No of Task',
			        data: result.stage_data

			    }]
			});
		});
		});
    	
    	// Sprint Hours Chart
    	$('.sprint_hours_bar_chart_btn').on('click', function(){
    		ajax.jsonRpc("/get_sprint_wise_data", 'call', {
    			'project_id': $('.sprint_wise_id').val(),
    		}).then(function(result) {
    			Highcharts.chart('sprint_hours_bar_chart', {
    			    chart: {
    			        type: 'column'
    			    },
    			    title:false,
    			    xAxis: {
    			        categories: result.sprint_data,
    			        crosshair: true
    			    },
    			    yAxis: {
    			        min: 0,
    			        title: {
    			            text: 'Hour(s)'
    			        }
    			    },
    			    plotOptions: {
    			        column: {
    			            pointPadding: 0.2,
    			            borderWidth: 0
    			        }
    			    },
    			    credits: {
    			        enabled: false
    			    },
    			    series: [{
    			        name: 'Estimated hours',
    			        data: result.expected_hrs

    			    },
    			    {
    			        name: 'Spent hours',
    			        data: result.effective_hrs

    			    }]
    			});
    		});
    	});
    	
    	// Team Load Bar Chart
    	$('.team_load_bar_btn').on('click', function(){
    		ajax.jsonRpc("/get_team_data", 'call', {
        		'project_id': $('.team_wise_id').val(),
    		}).then(function(result) {
    			Highcharts.chart('team_load_bar_chart', {
    			    chart: {
    			        type: 'column'
    			    },
    			    title:false,
    			    xAxis: {
    			        categories: result.team_member,
    			        crosshair: true
    			    },
    			    yAxis: {
    			        min: 0,
    			        title: {
    			            text: 'Workload hour(s)'
    			        }
    			    },
    			    plotOptions: {
    			        column: {
    			            pointPadding: 0.2,
    			            borderWidth: 0
    			        }
    			    },
    			    credits: {
    			        enabled: false
    			    },
    			    series: [{
    			        name: 'Load hour(s)',
    			        data: result.member_load

    			    }]
    			});
    		});
    	});
    	
    	// Team Load Pie Chart
    	$('.team_load_pie_btn').on('click', function(){
    		ajax.jsonRpc("/get_team_data", 'call', {
        		'project_id': $('.team_wise_id').val(),
    		}).then(function(result) {
    			var member_name = result.team_member
    			Highcharts.chart('team_load_pie_chart', {
    			    chart: {
    			        plotBackgroundColor: null,
    			        plotBorderWidth: null,
    			        plotShadow: false,
    			        type: 'pie'
    			    },
//    			    title: {
//    			        text: 'Browser market shares in January, 2018'
//    			    },
//    			    tooltip: {
//    			        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
//    			    },
    			    accessibility: {
//    			        point: {
//    			            valueSuffix: '%'
//    			        }
    			    },
    			    plotOptions: {
    			        pie: {
    			            allowPointSelect: true,
    			            cursor: 'pointer',
    			            dataLabels: {
    			                enabled: false,
    			                format: '<b>{member_name}</b>: {point.percentage:.1f} %'
    			            },
    			            showInLegend: true,
    			            
    			        }
    			    },
    			    series: [{
    			        name: 'No of Task',
    			        data: result.member_load
    			    }]
    			});
    		});
    	});
    	
    });
});