'''
<form action="" method="POST" id="consule">
        <fieldset>
            <legend>update to do</legend>
            <select name="task_name" id="">
                {%for task in tasks%}
                <option value="{{task[1]}}">{{task[1]}}</option>
                {% endfor %}
            </select>
            <input type="submit">
        </fieldset>
    </form>
    '''