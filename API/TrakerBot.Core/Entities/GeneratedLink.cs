namespace TrakerBot.Core.Entities;

public class GeneratedLink : BaseEntity
{
    public required string NewLink { get; set; }
    public required string ShortLink { get; set; }
    public required string Clicks { get; set; }

    // Navigation properties
    public required string OriginalLinkId { get; set; }
    public OriginalLink? OriginalLink { get; set; }
    public required string UserId { get; set; }
    public ApplicationUser? User { get; set; }
    
    // Many-to-many relationship with UTMs
    public ICollection<Utm>? Utms { get; set; }
}
