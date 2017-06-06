<!DOCTYPE HTML>
<html>
<head>
	<title>LED-Vote - Sample Page</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<meta property="og:title" content="LED-Vote - Sample Page" />
	<meta property="og:description" content="A sample page for the LED-Vote project" />
</head>
<body>
	<section>
		<h1>Take Over My LED Lights!</h1>
		<p><strong>Register, Sign-In, and Click on a colored LED to Vote</strong><br/>
		Once an LED Vote is received, the LED light will flash on my end!</p>
	</section>
	<hr/>
	<section>
		<div>
			<header>
				<h2>Log-In / Register</h2>
			</header>
			<p>Enter your username and password to login.<br/>
			Once registered and logged in, your voting data will be stored.</p>
		</div>
		<div>
			<strong id="notifier"></strong>
			<div id="entry_div">
				<div>
					<input type="text" name="entry_username" id="entry_username" value="" placeholder="username" />
				</div>
				<div>
					<input type="password" name="entry_secret" id="entry_secret" placeholder="password" />
					<input type="password" name="entry_secret_verify" id="entry_secret_verify" placeholder="verify password" style="display:none;" />
				</div>
				<div>
					<input type="submit" value="Login" onclick="login()" /></li>
					<input type="submit" value="Register" onclick="register()" /></li>
				</div>
			</div>
		</div>
	</section>
	<hr/>
	<section>
		<h1>Click to Vote</h1>
		<div>
			<ul id="led_select"></ul>
		</div>
		<div>
			<header>
					<h2>Your Votes</h2>
			</header>
			<div>
				<table>
					<thead>
						<tr>
							<th>Username</th>
							<th>Votes</th>
						</tr>
					</thead>
					<tbody id="user_votes_table"></tbody>
					<tfoot>
						<tr>
							<td colspan="1"></td>
							<td id="user_votes_table_calc"></td>
						</tr>
					</tfoot>
				</table>
			</div>
		</div>
	</section>
	<hr/>
	<section>
		<header>
			<h2>Total Votes</h2>
		</header>
		<div>
			<table>
				<thead>
					<tr>
						<th>Color</th>
						<th>Votes</th>
					</tr>
				</thead>
				<tbody id="total_votes_table"></tbody>
				<tfoot>
					<tr>
						<td colspan="1"></td>
						<td id="total_votes_table_calc"></td>
					</tr>
				</tfoot>
			</table>
		</div>
		<hr/>
		<div>
			<header>
				<h2>Top Users</h2>
			</header>
			<div>
				<table>
					<thead>
						<tr>
							<th>Username</th>
							<th>Total Votes</th>
							<th>Highest Voted</th>
						</tr>
					</thead>
					<tbody id="top_users_table"></tbody>
				</table>
			</div>
		</div>
	</section>
	<hr/>
	<footer>
		<ul>
			<li>This is a sample page for the <a href="https://github.com/FancyJesse/led-vote">LED-Vote</a> Project</li>
			<li>See a live and more decorated sample on <a href="http://ledvote.fancyjesse.com">LEDVote.FancyJesse.com</a></li>
		</ul>
	</footer>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<script type="text/javascript">
		var user_id = 0;
		var ledSelectList = document.getElementById('led_select');
		var userVotesTable = document.getElementById('user_votes_table');
		var totalVotesTable = document.getElementById('total_votes_table');
		var topUsersTable = document.getElementById('top_users_table');
		var notifier = document.getElementById('notifier');
		function verify(){
			var username = document.getElementById('entry_username').value.trim();
			var secret = document.getElementById('entry_secret').value.trim();
			if(username==''){
				notifier.innerHTML="Invalid username.";
                                return false;
                        }
                        if(secret==''){
                                notifier.innerHTML="Invalid password.";
                                return false;
                        }
                        return true;
                }
		function loggedIn(data){
			data = JSON.parse(data);
			user_id = data.user_id;
			notifier.innerHTML="Welcome, " + data.username + ".";
			$("#entry_div").hide();
			updateTables();
		}
                function login(){
                        if(verify()){
                                var username = document.getElementById('entry_username').value.trim();
                                var secret = document.getElementById('entry_secret').value.trim();
                                $.post('scripts/login.php', {'username':username, 'secret':secret},
                                        function(data){
                                                if(data!=0){
							loggedIn(data);
                                                } else {
                                                        notifier.innerHTML="Invalid username or password.";
                                                        user_id=0;
                                                }
                                        }
                                );
                        } else{
                                return false;
                        }
                }
                function register(){
                        if(verify()){
                                var username = document.getElementById('entry_username').value.trim();
                                var secret = document.getElementById('entry_secret').value.trim();
                                var secret_verify = document.getElementById('entry_secret_verify').value.trim();
                                if(secret_verify==''){
                                        notifier.innerHTML="Please re-enter your password to register.";
                                        document.getElementById('entry_secret_verify').style.display="inline";
                                        return false;
                                }
                                if(secret!=secret_verify){
                                        notifier.innerHTML="Passwords do not match.";
                                        return false;
                                }
                                $.post('scripts/register.php', {'username':username, 'secret':secret, 'secret_verify':secret_verify},
                                        function(data){
                                                if(data!=0){
							loggedIn(data);
                                                } else {
                                                        notifier.innerHTML="Failed to register. Username might be taken.";
                                                        user_id=0;
                                                }
                                        }
                                );
                        } else{
                                return false;
                        }
		}
		function updateTables(){
			$.ajax({
				type: 'POST',
				url: 'scripts/update.php',
				dataType: 'json',
				data: {'user_id':user_id},
				success: function (data) {
					calc(data);
				}
			});
			function calc(data){
				var user_votes = 0;
				var led_colors = {};
				var user_list = [];
				for(var k in data[0])
					if(!(k=='username'||k=='user_id'))
						led_colors[k] = 0;
				for(var i=0; i<data.length; i++){
					user = {}
					user['username'] = data[i].username;
					user['total_votes'] = 0;
					user['highest_voted'] = '';
					for(var color in led_colors){
						var num = parseInt(data[i][color]);
						user[color] = num;
						user['total_votes'] += num;
						led_colors[color] += num;
					}
					user_list.push(user);
					if(data[i].user_id==user_id)
						user_votes = user;
				}
				user_list.sort(function(a,b){return b['total_votes'] - a['total_votes']});
				display(user_votes, led_colors, user_list.slice(0,4));
			}
			function display(user_votes, total_votes, top_users){
				ledSelectList.innerHTML = '';
				ledSelectList.className = 'major-icons';
				for(var color in total_votes){
					var newColor = document.createElement('li');
					var newColorData = document.createElement('input');
					newColorData.type = 'button';
					newColorData.value = color;
					newColorData.style.color = '#C4C4C4';
					newColorData.style.backgroundColor = color;
					newColor.appendChild(newColorData);
					newColor.title = color;
					newColor.onclick = function(){
						this.childNodes[0].style.color = this.title;
						this.childNodes[0].style.backgroundColor="";
						vote(this.title);
					};
					ledSelectList.appendChild(newColor);
				}

				var userVotesHtml = '';
				var userVotesCnt = 0;
				if(user_votes==0){
					userVotesHtml = 'Please login to retrieve data.';
				}
				else{
					for(var color in total_votes){
						userVotesCnt += user_votes[color];
						userVotesHtml += '<tr><td>' + color + '</td><td>' + total_votes[color] + '</td></tr>';
					}
					document.getElementById('user_votes_table_calc').innerHTML = userVotesCnt;
				}
				userVotesTable.innerHTML = userVotesHtml;

				var totalVotesHtml = '';
				var totalVotesCnt = 0;
				for(var color in total_votes){
					totalVotesCnt += total_votes[color];
					totalVotesHtml += '<tr><td>' + color + '</td><td>' + total_votes[color] + '</td></tr>';
				}
				totalVotesTable.innerHTML = totalVotesHtml;
				document.getElementById('total_votes_table_calc').innerHTML = totalVotesCnt;

				var topUsersHtml = '';
				for(var i=0; i<top_users.length; i++){
					var highestVoted = '';
					for(var color in total_votes){
						if(highestVoted=='' || top_users[i][highestVoted]<top_users[i][color])
							highestVoted = color;
					}
					topUsersHtml += '<tr><td>' + top_users[i]['username'] + '</td><td>' + top_users[i]['total_votes'] + '</td><td>' + highestVoted + '</td></tr>';
				}
				topUsersTable.innerHTML = topUsersHtml;
			}
		}
		function vote(color){
			$.ajax({
				type: 'POST',
				url: 'scripts/vote.php',
				dataType: 'json',
				data: {'user_id':user_id, 'color_id':color},
				success: function (data) {
					updateTables();
				}
			});
		}
		updateTables();
	</script>
</body>
</html>
