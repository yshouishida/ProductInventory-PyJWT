using System;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows.Forms;
using prfProductInventory.Models;
using System.Collections.Generic;

namespace prfProductInventory.Forms
{
    public partial class frmMain : Form
    {
        private readonly HttpClient client = ApiClient.client;
        const string BASE_URL = "http://127.0.0.1:5000/api";
        public frmMain()
        {
            InitializeComponent();
        }

        private async Task GetCurrentUser()
        {
            try
            {
                HttpResponseMessage response = await client.GetAsync($"{BASE_URL}/me");
                string json = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    ApiResponse<User> result = JsonSerializer.Deserialize<ApiResponse<User>>(json);
                    User user = result.data;

                    tslblUser.Text = $"User: {user.last_name}, {user.first_name}";
                }
                else
                {
                    ApiResponse<User> result = JsonSerializer.Deserialize<ApiResponse<User>>(json); 

                    tslblUser.Text = $"Error: {result.message}";
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }

        private async void frmMain_Load(object sender, EventArgs e)
        {
            await GetCurrentUser();
            await LoadProducts();
        }

        //ADD
        private async void tsbtnAdd_Click(object sender, EventArgs e)
        {
            new frmProductDE().ShowDialog();

            await LoadProducts();
        }

        //UPDATE
        private async void tsbtnEdit_Click(object sender, EventArgs e)
        {
            if (dgvProductList.CurrentRow == null)
            {
                MessageBox.Show("Please select a record to edit.");
                return;
            }

            int productId = Convert.ToInt32(dgvProductList.CurrentRow.Cells["id"].Value);

            new frmProductDE(productId, true).ShowDialog();

            await LoadProducts();
        }

        //DELETE
        private async void tsbtnDelete_Click(object sender, EventArgs e)
        {
            if (dgvProductList.CurrentRow == null)
            {
                MessageBox.Show("Please select a record to delete.");
                return;
            }

            if (MessageBox.Show(
                "Do you want to delete this record?",
                "Confirmation",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Information
                ) == DialogResult.No)
            {
                return;
            }

            int productId = Convert.ToInt32(dgvProductList.CurrentRow.Cells["id"].Value);


            try
            {
                HttpResponseMessage response = await client.DeleteAsync($"{BASE_URL}/products/{productId}");
                string json = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    MessageBox.Show("Deleted successfully.");
                    await LoadProducts();
                }
                else
                {
                    MessageBox.Show(json, "Unable to delete");
                }

            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }


            await LoadProducts();


        }

        private async void tsBtnLogout_Click(object sender, EventArgs e)
        {
            if (MessageBox.Show(
                "Do you want to logout?",
                "Confirmation",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Information
                ) == DialogResult.Yes)
            {
                await Logout();
            }
        }

        private async Task LoadProducts()
        {
            try
            {
                HttpResponseMessage response = await client.GetAsync($"{BASE_URL}/products");
                string json = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    ApiResponse<List<Product>> products = JsonSerializer.Deserialize<ApiResponse<List<Product>>>(json);

                    dgvProductList.DataSource = products.data;
                }
                else
                {
                    MessageBox.Show(json, "Error");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }


        private async Task Logout()
        {
            try
            {
                HttpResponseMessage response = await client.PostAsync($"{BASE_URL}/logout", null);

                if (response.IsSuccessStatusCode)
                {
                    AuthSession.Clear();
                    ApiClient.ClearToken();

                    this.Close();
                    new frmLogin().Show();
                }
                else
                {
                    string error = await response.Content.ReadAsStringAsync();

                    MessageBox.Show(
                        error,
                        "Logout Error",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error
                    );
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    $"Error: {ex.Message}",
                    "Logout Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
        }
    }
}