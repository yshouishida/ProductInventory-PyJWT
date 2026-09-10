using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows.Forms;
using prfProductInventory.Models;

namespace prfProductInventory.Forms
{
    public partial class frmLogin : Form
    {
        private readonly HttpClient client = ApiClient.client;
        const string BASE_URL = "http://127.0.0.1:5000/api";

        public frmLogin() => InitializeComponent();

        private async void btnLogin_Click(object sender, EventArgs e) => await Login();

        private void btnClose_Click(object sender, EventArgs e) => this.Close();

        private void cbShowPwd_CheckedChanged(object sender, EventArgs e) => txtPassowrd.UseSystemPasswordChar = cbShowPwd.Checked ? false : true;

        private void frmLogin_Load(object sender, EventArgs e)
        {
        }

        private async Task Login()
        {
            try
            {
                User user = new User
                {
                    email = txtEmail.Text.Trim(),
                    password = txtPassowrd.Text
                };

                string json = JsonSerializer.Serialize(user);

                using (StringContent content = new StringContent(json, Encoding.UTF8, "application/json"))
                {
                    HttpResponseMessage response = await client.PostAsync($"{BASE_URL}/login", content);
                    string result = await response.Content.ReadAsStringAsync();


                    if (response.IsSuccessStatusCode)
                    {
                        ApiResponse<User> loginResponse = JsonSerializer.Deserialize<ApiResponse<User>>(result);

                        if (loginResponse == null || string.IsNullOrWhiteSpace(loginResponse.data.access_token))
                        {
                            MessageBox.Show(
                                $"Login token was not received.",
                                "Login error",
                                MessageBoxButtons.OK,
                                MessageBoxIcon.Error);
                            return;
                        }

                        AuthSession.AccessToken = loginResponse.data.access_token;

                        AuthSession.UserId = loginResponse.data.id;
                        AuthSession.FirstName = loginResponse.data.first_name;
                        AuthSession.LastName = loginResponse.data.last_name;
                        AuthSession.Email = loginResponse.data.email;


                        ApiClient.SetToken(AuthSession.AccessToken);

                        this.Hide();
                        new frmMain().ShowDialog();
                    }
                    else
                    {
                        ApiResponse<User> loginResponse = JsonSerializer.Deserialize<ApiResponse<User>>(result);
                        MessageBox.Show(
                            loginResponse.message,
                            "Login error",
                            MessageBoxButtons.OK,
                            MessageBoxIcon.Error);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    $"Error: {ex.Message}",
                    "Internal error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
        }

    }
}
