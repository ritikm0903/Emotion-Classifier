import streamlit as st

def maximize_page():
    html_code = """
    <style>
    #maximize-button {
        position: fixed;
        background-color: red;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    #main{
        width: 80vw;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background: linear-gradient(135deg, #3498db, #8e44ad); /* Linear gradient background */
    color: #fff; /* White text color for better contrast */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    </style>
    <button onclick="toggleFullscreen()" id="maximize-button">Maximize</button>
    <div id="main">
    <h1>Depression Measurement Assessment</h1>
    <p>Over the last two weeks, how often have you been bothered by any of the following problems?</p>
    <div>
        <p>1. Little interest or pleasure in doing things</p>
        <input type="radio" name="question_1" value="0"> Not at all(0 points)
        <input type="radio" name="question_1" value="1"> Several days(1 points)
        <input type="radio" name="question_1" value="2"> More than half the days(2 points)
        <input type="radio" name="question_1" value="3"> Nearly every day(3 points)
    </div>
    <div>
        <p>2. Feeling down, depressed, or hopeless</p>
        <input type="radio" name="question_2" value="0"> Not at all(0 points)
        <input type="radio" name="question_2" value="1"> Several days(1 points)
        <input type="radio" name="question_2" value="2"> More than half the days(2 points)
        <input type="radio" name="question_2" value="3"> Nearly every day(3 points)
    </div>
    <div>
        <p>3. Trouble falling or staying asleep, or sleeping too much</p>
        <input type="radio" name="question_3" value="0"> Not at all(0 points)
        <input type="radio" name="question_3" value="1"> Several days(1 points)
        <input type="radio" name="question_3" value="2"> More than half the days(2 points)
        <input type="radio" name="question_3" value="3"> Nearly every day(3 points)
    </div>
    <div>
        <p>4. Feeling tired or having little energy</p>
        <input type="radio" name="question_4" value="0"> Not at all(0 points)
        <input type="radio" name="question_4" value="1"> Several days(1 points)
        <input type="radio" name="question_4" value="2"> More than half the days(2 points)
        <input type="radio" name="question_4" value="3"> Nearly every day(3 points)
    </div>
    <div>
        <p>5. Poor appetite or overeating</p>
        <input type="radio" name="question_5" value="0"> Not at all(0 points)
        <input type="radio" name="question_5" value="1"> Several days(1 points)
        <input type="radio" name="question_5" value="2"> More than half the days(2 points)
        <input type="radio" name="question_5" value="3"> Nearly every day(3 points)
    </div>
    <div>
        <p>6. Feeling bad about yourself, or that you are a failure, or have let yourself or your family down</p>
        <input type="radio" name="question_6" value="0"> Not at all(0 points)
        <input type="radio" name="question_6" value="1"> Several days(1 points)
        <input type="radio" name="question_6" value="2"> More than half the days(2 points)
        <input type="radio" name="question_6" value="3"> Nearly every day(3 points)
    </div>
    <div>
        <p>7. Trouble concentrating on things, such as reading the newspaper or watching television</p>
        <input type="radio" name="question_7" value="0"> Not at all(0 points)
        <input type="radio" name="question_7" value="1"> Several days(1 points)
        <input type="radio" name="question_7" value="2"> More than half the days(2 points)
        <input type="radio" name="question_7" value="3"> Nearly every day(3 points)
    </div>
    <div>
        <p>8. Moving or speaking so slowly that other people could have noticed? Or the opposite, being so fidgety or restless that you have been moving around a lot more than usual</p>
        <input type="radio" name="question_8" value="0"> Not at all(0 points)
        <input type="radio" name="question_8" value="1"> Several days(1 points)
        <input type="radio" name="question_8" value="2"> More than half the days(2 points)
        <input type="radio" name="question_8" value="3"> Nearly every day(3 points)
    </div>
    <div>
        <p>9. Thoughts that you would be better off dead or of hurting yourself in some way</p>
        <input type="radio" name="question_9" value="0"> Not at all(0 points)
        <input type="radio" name="question_9" value="1"> Several days(1 points)
        <input type="radio" name="question_9" value="2"> More than half the days(2 points)
        <input type="radio" name="question_9" value="3"> Nearly every day(3 points)
    </div>
    
    <div>
        <button onclick="calculateTotalPoints()">Calculate Total Points</button>
        <p id="total_points"></p>
        <p id="score_range_label" style="font-weight: bold;"></p>
    </div>
</div>




    <script>
    
       function calculateTotalPoints() {
        var totalPoints = 0;
        var radios = document.querySelectorAll('input[type="radio"]:checked');
        radios.forEach(function(radio) {
            totalPoints += parseInt(radio.value);
        });
        document.getElementById('total_points').innerHTML = "Total criteria point count: " + totalPoints;

        var scoreRangeLabel = document.getElementById('score_range_label');
        if (totalPoints >= 25 && totalPoints <= 30) {
            scoreRangeLabel.textContent = "The person should be mandated to undergo medical treatment.";
            scoreRangeLabel.style.color = "red";
        } else if (totalPoints >= 20 && totalPoints < 25) {
            scoreRangeLabel.textContent = "They require surveillance";
            scoreRangeLabel.style.color = "orange";
        } else if (totalPoints >= 15 && totalPoints < 20) {
            scoreRangeLabel.textContent = "Daily checkups are necessary for them.";
            scoreRangeLabel.style.color = "yellow";
        } else if (totalPoints >= 10 && totalPoints < 15) {
            scoreRangeLabel.textContent = "The person needs to be handled with care.";
            scoreRangeLabel.style.color = "greenyellow";
        } else if (totalPoints >= 0 && totalPoints < 10) {
            scoreRangeLabel.textContent = "Normal";
            scoreRangeLabel.style.color = "green";
        } else {
            scoreRangeLabel.textContent = ""; // Clear label if total points are invalid
        }
    }
   
    var isFullscreen = false;
    function toggleFullscreen() {
        var elem = document.documentElement;
        if (!isFullscreen) {
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) { /* Safari */
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) { /* IE11 */
                elem.msRequestFullscreen();
            }
            document.getElementById('maximize-button').innerHTML = 'Minimize';
            isFullscreen = true;
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) { /* Safari */
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) { /* IE11 */
                document.msExitFullscreen();
            }
            document.getElementById('maximize-button').innerHTML = 'Maximize';
            isFullscreen = false;
        }
    }
    </script>
    """
    st.components.v1.html(html_code)

# def depression_assessment():
#     st.title("Depression Measurement Assessment")
#     st.write("Over the last two weeks, how often have you been bothered by any of the following problems?")
    
#     questions = [
#         "Little interest or pleasure in doing things",
#         "Feeling down, depressed, or hopeless",
#         "Trouble falling or staying asleep, or sleeping too much",
#         "Feeling tired or having little energy",
#         "Poor appetite or overeating",
#         "Feeling bad about yourself, or that you are a failure, or have let yourself or your family down",
#         "Trouble concentrating on things, such as reading the newspaper or watching television",
#         "Moving or speaking so slowly that other people could have noticed? Or the opposite, being so fidgety or restless that you have been moving around a lot more than usual",
#         "Thoughts that you would be better off dead or of hurting yourself in some way"
#     ]
    
#     total_points = 0
#     for i, question in enumerate(questions):
#         response = st.radio(f"{i+1}. {question}", options=["Not at all(0 points)", "Several days(1 points)", "More than half the days(2 points)", "Nearly every day(3 points)"])
#         if response == "Not at all(0 points)":
#             points = 0
#         elif response == "Several days(1 points)":
#             points = 1
#         elif response == "More than half the days(2 points)":
#             points = 2
#         elif response == "Nearly every day(3 points)":
#             points = 3
        
#         st.write(f"Selected response: {response} - Points: {points}")
#         total_points += points
    
#     st.write(f"Total criteria point count: {total_points}")

if __name__ == "__main__":
    maximize_page()

