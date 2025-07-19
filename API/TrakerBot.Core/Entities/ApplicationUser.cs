using Microsoft.AspNetCore.Identity;

namespace TrakerBot.Core.Entities;

public class ApplicationUser : IdentityUser
{
    public string? FirstName { get; set; }
    public string? LastName { get; set; }
    public string? ProfilePictureUrl { get; set; }
    public DateTime DateOfBirth { get; set; }

    // Navigation properties
    public ICollection<Telegram>? Telegrams { get; set; }
    public ICollection<OriginalLink>? OriginalLinks { get; set; }
    public ICollection<Utm>? Utms { get; set; }

}
