def add_custom_styles():
    st.markdown(
        """
        <style>
        .stApp { 
            background-image: url('https://r4.wallpaperflare.com/wallpaper/142/751/831/landscape-anime-digital-art-fantasy-art-wallpaper-9b468c3dc3116f4905f43bc9cddc0cf0.jpg');  
            background-size: cover;
            background-position: center center;
            color: white;
        }

        h1, h2, h3, h4 {
            text-align: center;
            color: #FFFFFF;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        }

        .stButton > button {
            background-color: #1C1C1C;  /* Matte black background */
            color: white;  /* White text for contrast */
            border-radius: 12px;
            padding: 10px;
            font-size: 16px;
            transition: 0.3s ease;
            border: none;
        }

        .stButton > button:hover {
            background-color: #333333;  /* Slightly lighter black on hover */
        }

        .stExpander {
            background-color: rgba(62, 42, 71, 0.9);  /* Dark Purple with slight transparency */
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.4);  /* Subtle shadow for depth */
            font-size: 18px;
            color: #FFFFFF;  /* White text for contrast */
        }

        .stExpander header {
            font-size: 18px;
            font-weight: bold;
            color: #F9D539;  /* Yellow for the header text */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }

        .questions-submitted-card {
            background-color: rgba(62, 42, 71, 0.8);  /* Dark purple, slightly transparent */
            color: #F9D539;  /* Yellow text for contrast */
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
