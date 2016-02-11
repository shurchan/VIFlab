/*=====================
 -- Pixl --
 
 Created for CodeCanyon
 by FV iMAGINATION
 =====================*/

#import "CLImageToolBase.h"

@implementation CLImageToolBase

- (id)initWithImageEditor:(_CLImageEditorViewController*)editor withToolInfo:(CLImageToolInfo*)info
{
    self = [super init];
    if(self){
        self.editor   = editor;
        self.toolInfo = info;
    }
    return self;
}

+ (NSString*)defaultIconImagePath
{
    return [NSString stringWithFormat:@"%@.bundle/%@/icon.png", [CLImageEditorTheme bundleName], NSStringFromClass([self class])];
}

+ (CGFloat)defaultDockedNumber
{
    // Image tools are sorted according to the dockedNumber in tool bar.
    // Override point for tool bar customization
    NSArray *tools = @[
                       @"CLFilterTool",
                       @"CLBrightnessTool",
                       @"CLSaturationTool",
                       @"CLContrastTool",
                       @"CLEffectTool",
                       @"CLBlurTool",
                       @"CLRotateTool",
                       @"CLClippingTool",
                       @"CLToneCurveTool",
                       @"CLSplashTool",
                       @"CLFramesTool",

                       ];
    return [tools indexOfObject:NSStringFromClass(self)];
}

+ (NSArray*)subtools
{
    return nil;
}

+ (NSString*)defaultTitle
{
    return @"DefaultTitle";
}

+ (BOOL)isAvailable
{
    return false;
}

+ (NSDictionary*)optionalInfo
{
    return nil;
}

#pragma mark - SETUP ====================

- (void)setup
{


}

- (void)cleanup
{
    
}

- (void)executeWithCompletionBlock:(void(^)(UIImage *image, NSError *error, NSDictionary *userInfo))completionBlock
{
    completionBlock(self.editor.imageView.image, nil, nil);
}

- (UIImage*)imageForKey:(NSString*)key defaultImageName:(NSString*)defaultImageName {
    NSString *iconName = self.toolInfo.optionalInfo[key];
    
    if(iconName.length>0){
        return [UIImage imageNamed:iconName];
    } else {
        return [CLImageEditorTheme imageNamed:[NSString stringWithFormat:@"%@", [self class]]];
    }
}


@end
