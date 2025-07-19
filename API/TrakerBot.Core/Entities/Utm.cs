namespace TrakerBot.Core.Entities;

public class Utm : BaseEntity
{
    public required string Name { get; set; }
    public required string Value { get; set; }
    public string? UserId { get; set; }
    public ApplicationUser? User { get; set; }
}
