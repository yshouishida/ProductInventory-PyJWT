namespace prfProductInventory.Forms
{
    class AuthSession
    {
        public static string AccessToken { get; set; }
        public static int UserId { get; set; }
        public static string FirstName { get; set; }
        public static string LastName { get; set; }
        public static string Email { get; set; }

        public static void Clear()
        {
            AccessToken = null;
            UserId = 0;
            FirstName = null;
            LastName = null;
            Email = null;
        }
 
    }
}
