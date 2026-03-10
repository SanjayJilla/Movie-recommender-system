mkdir -p ~/.streamlit/

echo "/
[server]\n\
port=$PORt\n\
enableCORS=false\n\
headless=true\n\
\n\
" > ~/.streamlit/config.toml