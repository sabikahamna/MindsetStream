import streamlit as st
import pandas as pd 
import os
from io import BytesIO
  

st.set_page_config(page_title=" Data sweeper", layout = 'wide')

st.title("Data sweeper")
st.write("transfrom yur files between CSV and Excel formats with built-in data cleaning and visualization!")


uploaded_files = st.file_uploader(
    "Upload your files (CSV or EXCEL):", 
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue


        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size :**{file.size/1524}")


        st.write("preview the Head of the Dataframe")
        st.dataframe(df.head())

        st.subheader("Data cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
            with col2:
                if st.button(f"Full Missing Value For {file.name}"):
                    numeric_cols = df.select_dtypes(include=['numbers']).columns
                    df [numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Value have been filled! ")

# choose specific columns to keep or convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect("choose columns for {file.name}", df.columns,default=df.columns)
        df = df[columns]

      #create some visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


            #convert the file -> CSV TO EXCEL

            st.subheader(" Conversation Option")
            conversion_type = st.radio("Convert {file.name} to:" , ["CSV","Excel"], key=file.name)
            if st.button("Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer,index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index = False)
                    file_name = file.name.replace(file_ext,".Xlsx")
                    mime_type = "mime_type = ""application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)


                    #Downlaod Button
                    st.download_button(
                        label = f"download { file.name} as {conversion_type}",
                        data=buffer,
                        file_name=file_name,
                        mime=mime_type
                    )
                    
            st.success("All files processed!")