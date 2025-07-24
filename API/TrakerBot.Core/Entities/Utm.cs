namespace TrakerBot.Core.Entities;

public class Utm : BaseEntity
{
    public required string Name { get; set; }
    public required string Value { get; set; }
    public string? Source { get; set; }
    public string? Medium { get; set; }
    public string? Campaign { get; set; }
    public string? UserId { get; set; }
    public ApplicationUser? User { get; set; }
    
    // Many-to-many relationship with GeneratedLinks
    public ICollection<GeneratedLink>? GeneratedLinks { get; set; }
}
