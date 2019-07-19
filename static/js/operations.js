function finger_add()
{

	$.ajax(
	{
		type: "POST",
		url: "/finger_add",
		dataType: "html",
		success: function(msg)
		{
			console.log(msg);
			$("#display").html(msg);
		},
		error: function (xhr, status, error) 
		{
			console.log(error);
		}
	});

}

function finger_sub()
{
	$.ajax(
	{
		type: "POST",
		url: "/finger_sub",
		dataType: "html",
		success: function(msg)
		{
			console.log(msg);
			$("#display").html(msg);
		},
		error: function (xhr, status, error)
		{
			console.log(error);
		}
	});
}

function finger_mul()
{
	$.ajax(
	{
		type: "POST",
		url: "/finger_mul",
		dataType: "html",
		success: function(msg)
		{
			console.log(msg);
			$("#display").html(msg);
		},
		error: function (xhr, status, error)
		{
			console.log(error);
		}
	});
}

function finger_div()
{
	$.ajax(
	{
		type: "POST",
		url: "/finger_div",
		dataType: "html",
		success: function(msg)
		{
			console.log(msg);
			$("#display").html(msg);
		},
		error: function (xhr, status, error) 
		{
			console.log(error);
		}
	});
}
