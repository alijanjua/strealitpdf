import streamlit as st
import os
import dropbox
from dropbox.files import WriteMode
from dropbox.sharing import RequestedVisibility
from pathlib import Path

# --- Inject CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

import streamlit as st

# Inject custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Replace this with your Dropbox access token
#DROPBOX_ACCESS_TOKEN = "sl.u.AF0Plr2rAbcSbViajFxw3KopLy-Xng0HK_Ks68oSMGjv0xpK1kHfhhTUJLNnBz511cQn5d2rgGxp_aKA3AqgXACDFXVvDpIdXEXH_MK5U79WWB3YXmDjrfrd8fRTIe6H2KhVdsGTMNM2fQgx7fMg8K-1Qh3JPxJqn_eCsUTjvR355ui8CxuG1KJChrFhUDtRlBO72zbUY6cjCr8U98jOPvBL6OdWznFqz2bNUpFIf8PiszRZZv7EoZl-CBrdipt8iArrgYqjEwBNxIlWlRaEUMQVRG3jRhF3GWp7NPGSO76KUoGx4s6i23p9_2IEi-Mch7vSHrXOAg-SnRN-FOqetnpoWJ6T3MPFnuNA8ZzyaLneGlnc5552u5wSMucePraLgK60O4qW8NxYExRfXdC7gapW9co1TuqC5kZ7cpD7KNVlPp8qOurcKTX6pv9ZpAZ-03T26GqsCSlbxd0fXYlKuuGDtcmFzr7d-plNmL4p_U-2TJCYyuMxi9qOhciJiVKt3yCNNGDZOxrb5RFCiB6p16Sq4qEbR1YkI7XEodpNNzY7emEd3Us5ySmGqTbymP4dw65kzkIZR7w2by569k1jgI0zB7nUXp66VpeKKtsVj-tnVPtQSaSj5VBDirZWiO7NoObwvKAn11hask10nrZeCIRYy2p0JvYeGEI6XjCGW8AQyIrli13CXBQ8nK68vYeJ_5vS9-Dk6Ic3l9zlpZbMUPARB9nPqNpGZDZnYcUJviddHPaP_rDKwrjQ4blQT0CcjQqnC2rsYxfAKxOpAOArghJlO_YUl8q8VjUUrvTPFXncRWqzeNOFMNeFzI40V7DC82ce_mUm-keSQLDu8Vsj5Fh1368BbvtrPkfs6rX6Tj1PXhFX1BrxUqot3oO9dxqG6H3OACUSc1ZnsKM3wVIYRCv3cQEx5utIHZji8gIC2zH0EUVGJByH5O1Mt9cUrVmtQckfBjiyQOLULziRpTog-UPmS7lJ72Ne3VQzmcYErJUhpFboauTIppxVuyb7pX-lAOlfjsrqgWCb6uLkqHGRHvkHedwFmtXSauc3CxoDc-bkEfPHUk35_7BEwpZE2NWKHK5dnqUryX2Gh0ROTOy0S06pUMfNYaus-tweYvOoHWkxQAdPNLKSo9l4sedV7dNysFimJoudKN1-HAgI68q5ZftvblBPtSZ4H3AfjAnjt3BhpFSq1L_r1EaKV0Yo0sj9KdQLzSoWwksKxnorG5jSIntjtE9RcqWZmKHRx5BDmqF6xoRWTuSEQwaJy2o9R6ibY9fKD0qExIDxkWVnBSPPL138"
access_token = st.secrets["dropbox"]["access_token"]
dbx = dropbox.Dropbox(access_token)

# Initialize Dropbox client
dbx = dropbox.Dropbox(access_token)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About", "Contact"])

if page == "Home":
    st.title("🏠 Upload PDF to Dropbox")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        try:
            file_name = uploaded_file.name
            file_bytes = uploaded_file.getvalue()
            dropbox_path = f"/{file_name}"

            # Upload to Dropbox (overwrite if it exists)
            dbx.files_upload(file_bytes, dropbox_path, mode=WriteMode("overwrite"))
            st.success("✅ File uploaded to Dropbox!")

            # Try to get existing shared link
            links = dbx.sharing_list_shared_links(path=dropbox_path, direct_only=True).links

            if links and len(links) > 0:
                shared_link_url = links[0].url
            else:
                shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
                dropbox_path,
                settings=dropbox.sharing.SharedLinkSettings(
                    requested_visibility=RequestedVisibility.public
                    )
                )
                shared_link_url = shared_link_metadata.url

            # Show the shareable link
            st.markdown(f"🔗 [Click here to open your file]({shared_link_url})")
            st.info("You can share this link with others.")

        except Exception as e:
            st.error("❌ Error uploading or sharing file:")
            st.exception(e)


elif page == "About":
    st.title("ℹ️ About")
    st.write("This app uploads your PDF to Dropbox and gives you a public link.")

elif page == "Contact":
    st.title("✉️ Contact")
    st.write("Reach us at contact@example.com")
