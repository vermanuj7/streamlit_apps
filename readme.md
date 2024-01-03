```python
import streamlit as st
import pandas as pd
import numpy as np
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])

st.line_chart(chart_data)
```

### access session state using widget key
```python
import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
ssn_state_name = st.session_state.name
print(ssn_state_name)
```
### Use checkbox to show/hide widgets
```python
import streamlit as st
import numpy as np
import pandas as pd

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data
```

### Layout - add elements to sidebar
```python
import streamlit as st

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
```

Beyond the sidebar, Streamlit offers several other ways to control the layout of your app. st.columns lets you place
widgets side-by-side, and st.expander lets you conserve space by hiding away large content.

```python
import streamlit as st

left_column, right_column = st.columns(2)

# You can use a column just like st.sidebar:

left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:

with right_column:
    chosen = st.radio(
    'Sorting hat',
    ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")
```
