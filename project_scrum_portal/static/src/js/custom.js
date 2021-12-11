odoo.define('project_scrum_portal.scrum_portal', function (require) {
"use strict";
    var core = require('web.core');
    var ajax = require('web.ajax');
    document.onload = function () {
        if ($('#sprint_id').val()) {

        	ajax.jsonRpc("/get_sprint_data", 'call', {
            	'sprint_id': $('.sprints').val(),
            }).then(function(result) {
            	var chart = new CanvasJS.Chart("chartContainer", {
            		theme: "light2",
            		title:{
//		            	text: "Burndownchart"
            		},
            		exportEnabled: true,
            		width:800,
            		data: [  //array of dataSeries     
        			{ //dataSeries - first quarter
        				/*** Change type "column" to "bar", "area", "line" or "pie"***/
        				type: "line",
        				name: "Remaining Points",
        				showInLegend: true,
        				dataPoints: result['remaining_points']
        			},
        			{ //dataSeries - second quarter
        				type: "line",
        				name: "Hours Left", 
        				showInLegend: true,               
        				dataPoints: result['remaining_hours']
        			}
        			],
            	});
		        chart.render();
			});
    		
        	ajax.jsonRpc("/get_sprint_data", 'call', {
        		'sprint_id': $('.sprints').val(),
        	}).then(function(result) {
        		var chart = new CanvasJS.Chart("chartContainer2", {
        			theme: "light2",
        			exportEnabled: true,
        			width:800,
        			data: [  //array of dataSeries     
    				{ //dataSeries - first quarter
    					/*** Change type "column" to "bar", "area", "line" or "pie"***/
    					type: "column",
    					name: "Remaining Points",
    					showInLegend: true,
    					dataPoints: result['remaining_points']
    				},
    				{ //dataSeries - second quarter
    					type: "column",
    					name: "Hours Left", 
    					showInLegend: true,
    					dataPoints: result['remaining_hours']
    				}
    				],
        		});
        		chart.render();
        	});
			
			ajax.jsonRpc("/get_sprint_data", 'call', {
	    		'sprint_id': $('.sprints').val(),
    		}).then(function(result) {
    			var chart = new CanvasJS.Chart("chartContainer1", {
    				theme: "light2", // "light2", "dark1", "dark2"
    				animationEnabled: false, // change to true		
    				exportEnabled: true,
    				width:800,
    				data: [
    				{
    					type: "pie",
    					toolTipContent: "{label}: <strong>{y}</strong>",
    					indexLabel: "{label} : {y}",
    					dataPoints: result['remaining_points']
    				}
    				]
    			});
    			chart.render();
    		});
        }
        
    	
    	ajax.jsonRpc("/get_team_data", 'call', {
    		'project_id': $('.team_wise_id').val(),
		}).then(function(result) {
			var chart = new CanvasJS.Chart("chartteam1", {
				theme: "light2", // "light2", "dark1", "dark2"
				animationEnabled: false, // change to true		
				exportEnabled: true,
				width:800,
				data: [
				{
					type: "pie",
					toolTipContent: "{label}: <strong>{y}</strong>",
					indexLabel: "{label} : {y}",
					dataPoints: result
				}
				]
			});
			chart.render();
		});
    };	

    $(document).on('change', '#sprint_id', function(){
    	ajax.jsonRpc("/get_sprint_data", 'call', {
    		'sprint_id': $(this).val(),
		}).then(function(result) {
			var chart = new CanvasJS.Chart("chartContainer", {
				theme: "light2",
				exportEnabled: true,
				width:800,
				title:{
//  		       text: "Burndownchart"
				},
				data: [  //array of dataSeries     
				{ //dataSeries - first quarter
					/*** Change type "column" to "bar", "area", "line" or "pie"***/
  		           	type: "line",
  		           	name: "Remaining Points",
  		           	showInLegend: true,
  		           	dataPoints: result['remaining_points']
	         	},
	         	{ //dataSeries - second quarter
	         		type: "line",
	         		name: "Hours Left", 
	         		showInLegend: true,               
	         		dataPoints: result['remaining_hours']
	        	}
  		        ],
			});
			chart.render();
		});
    })
    
    $(document).on('change', '#sprint_id', function(){
    	ajax.jsonRpc("/get_sprint_data", 'call', {
    		'sprint_id': $(this).val(),
		}).then(function(result) {
			var chart = new CanvasJS.Chart("chartContainer2", {
				theme: "light2",
				exportEnabled: true,
				width:800,
				data: [  //array of dataSeries     
				{ //dataSeries - first quarter
					/*** Change type "column" to "bar", "area", "line" or "pie"***/
					type: "column",
					name: "Remaining Points",
					showInLegend: true,
					dataPoints: result['remaining_points']
				},
				{ //dataSeries - second quarter
					type: "column",
					name: "Hours Left", 
					showInLegend: true,               
					dataPoints: result['remaining_hours']
		        }
		        ],
			});
			chart.render();
		});
    });
    
    $(document).on('change', '#sprint_id', function(){
    	ajax.jsonRpc("/get_sprint_data", 'call', {
    		'sprint_id': $(this).val(),
		}).then(function(result) {
			var chart = new CanvasJS.Chart("chartContainer1", {
				theme: "light2",
				exportEnabled: true,
				width:800,
				data: [  //array of dataSeries     
				{ //dataSeries - first quarter
					/*** Change type "column" to "bar", "area", "line" or "pie"***/
  		           	type: "pie",
  		           	toolTipContent: "{label}: <strong>{y}</strong>",
  		           	indexLabel: "{label} : {y}",
  		           	name: "Remaining Points",
  		           	showInLegend: true,
  		           	dataPoints: result['remaining_points']
	         	},
  		        ],
			});
			chart.render();
		});
    });

    $(function () {
        var kanbanCol = $('.panel-body');
//        kanbanCol.css('max-height', (window.innerHeight - 150) + 'px');
        var kanbanColCount = parseInt(kanbanCol.length);
        $('.kanban-container-fluid').css('min-width', (kanbanColCount * 350) + 'px');
        draggableInit();
        $('.kanban-col').on('click', function() {
            $(this).toggleClass('clicked');
        });
    });

    function draggableInit() {
        var sourceId;
        var taskId;

        $('[draggable=true]').bind('dragstart', function (event) {
            sourceId = $(this).parent().attr('id');
            taskId = $(this).attr('id')
            event.originalEvent.dataTransfer.setData("text/plain", event.target.getAttribute('id'));
        });

        $('.panel-body').bind('dragover', function (event) {
            event.preventDefault();
        });

        $('.panel-body').bind('drop', function (event) {
            var children = $(this).children();
            var targetId = children.attr('id');
             ajax.jsonRpc("/update_sprint_stage", 'call', {
        		'sprint_id': taskId,
        		'source_id': sourceId,
        		'target_id': targetId,
            }).then(function(res) {
            	if(res){
            		location.reload();
            	} else {
            	    alert("sorry!!!!! not value in json call")
            	}
            });
            ajax.jsonRpc("/update_backlog_stage", 'call', {
            	'backlog_id': taskId,
         		'source_id': sourceId,
         		'target_id': targetId,
            }).then(function(res) {
             	if(res){
             		location.reload();
             	} else {
             	    alert("sorry!!!!! not value in json call")
             	}
            });
            if (sourceId != targetId) {
                var elementId = event.originalEvent.dataTransfer.getData("text/plain");
                $('#processing-modal').modal('toggle'); //before post
                // Post data 
                setTimeout(function () {
                    var element = document.getElementById(elementId);
                    children.prepend(element);
                    $('#processing-modal').modal('toggle'); // after post
                }, 1000);
            }
            event.preventDefault();
        });
    }

	$(document).ready(function() {
        $('#StartdatePicker').datepicker({
            format: 'yyyy-mm-dd'
        });
        $('#EnddatePicker').datepicker({
        	format: 'yyyy-mm-dd'
        });
        $('#AskdatePicker').datepicker({
        	format:'yyyy-mm-dd'
        });
		$('#media').carousel({
		    pause: true,
		    interval: false,
		});
	});
 });

	//optional
	$('#blogCarousel').carousel({
		interval: 500000
	});